from flask import (Flask, Blueprint, flash, g, redirect, render_template, request, url_for, jsonify)
from werkzeug.exceptions import abort

from courseme.auth import login_required
from courseme.db import get_db, search_courses

from datetime import datetime, timedelta

import re, random

bp = Blueprint('courses', __name__)

@bp.route('/')
def index():
    return render_template('courses/index.html')

@bp.route('/survey', methods=('GET', 'POST'))
@login_required
def survey():
    user_id = g.user['id']
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM concentrations")
    concentrationslist = cursor.fetchall()
    cursor.execute("SELECT * FROM secondaries")
    secondarieslist = cursor.fetchall()

    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form.get('email')
        concentration_type = request.form['concentration_type']
        concentration1_id = request.form['concentration1']
        concentration2_id = request.form.get('concentration2')
        secondary_type = request.form.get('secondary_type')
        secondary_id = request.form.get('secondary')
        year = request.form['year']
        current_semester = request.form['current_semester']
        semesters_completed = request.form['semesters_completed']
        num_courses_want = request.form['num_courses_want']
        want_gened = request.form['want_gened']
        want_grad = request.form['want_grad']
        want_9am = request.form['want_9am']
        want_conc_req = request.form['want_conc_req']

        semesters = {}
        for key, value in request.form.items():
            if key.startswith('course_'):  # Look for keys like 'course_1_0', 'course_2_1', etc.
                parts = key.split('_')  # Split into ['course', semesterNumber, courseIndex]
                semester_number = int(parts[1])
                course_index = int(parts[2])

                if semester_number not in semesters:
                    semesters[semester_number] = []
                semesters[semester_number].append(value)  # Add course to the corresponding semester

        error = None

        # Validate the form fields
        if not first_name:
            error = 'First name is required.'
        elif not last_name:
            error = 'Last name is required.'
        elif not concentration_type:
            error = 'Concentration type is required.'
        elif not concentration1_id:
            error = 'Concentration is required.'
        elif not secondary_type:
            error = 'Secondary type is required.'
        elif not year:
            error = 'Year is required.'
        elif not current_semester:
            error = 'Current semester is required.'
        elif not semesters_completed:
            error = 'Semesters completed is required.'
        elif not num_courses_want:
            error = 'Number of courses for next semester is required.'
        elif not want_gened:
            error = 'GenEd preference is required.'
        elif not want_grad:
            error = 'Graduate course preference is required.'
        elif not want_9am:
            error = '9am preference is required.'
        elif not want_conc_req:
            error = 'Concentration requirements preference is required.'

        want_gened = request.form.get('want_gened') == 'Yes'
        want_grad = request.form.get('want_grad') == 'Yes'
        want_9am = request.form.get('want_9am') == 'Yes'
        want_conc_req = request.form.get('want_conc_req') == 'Yes'

        if error is None:
            try:
                # Only insert into profiles table without updating
                db.execute("""
                    INSERT INTO profiles (user_id, first_name, last_name, email, concentration1_id, concentration2_id, secondary_id, 
                                         year, current_semester, num_courses_want, want_gened, want_grad, want_9am, want_conc_req)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (user_id, first_name, last_name, email, concentration1_id, concentration2_id, secondary_id, year, current_semester,
                      num_courses_want, want_gened, want_grad, want_9am, want_conc_req))
                
                # Insert into user_courses table for each semester and course
                for semester_number, courses in semesters.items():
                    for full_course_name in courses:
                        if ":" in full_course_name:
                            _, course_name = full_course_name.split(":", 1)
                            course_name = course_name.strip()  # Remove any extra spaces
                        else:
                            course_name = full_course_name.strip()

                        # Get course_id for the course name (insert if not exists)
                        cursor.execute(
                            "SELECT id FROM courses WHERE title = ?",
                            (course_name,)
                        )
                        course = cursor.fetchone()

                        if not course:
                            db.execute("INSERT INTO courses (title) VALUES (?)", (course_name,))
                            cursor.execute("SELECT id FROM courses WHERE title = ?", (course_name,))
                            course = cursor.fetchone()

                        course_id = course['id']

                        # Insert into user_courses table
                        db.execute("""
                            INSERT INTO user_courses (user_id, course_id, semester, year)
                            VALUES (?, ?, ?, ?)
                        """, (user_id, course_id, semester_number, year))

                db.commit()
                return redirect(url_for("courses.courses"))
            except db.IntegrityError as e:
                error = f"IntegrityError: {e}"

    return render_template('courses/survey.html', concentrationslist=concentrationslist, secondarieslist=secondarieslist)

def parse_course_code(catalog_number):
    """
    Parse a course code into numeric and alphabetic parts.
    Handles cases where course codes are only numbers, only letters, or a mix of both.
    """
    match = re.match(r'(\d+)?([A-Za-z]+)?', catalog_number)
    if match:
        number = int(match.group(1)) if match.group(1) else None
        letters = match.group(2) if match.group(2) else None
        return number, letters
    raise ValueError("Invalid catalog_number format")

# Converts a time string into datetime
def time_to_datetime(time_str):
    if not time_str:
        return None
    try:
        return datetime.strptime(time_str, "%H:%M")
    except ValueError:
        return None

# Checks if the times themselve overlap
def check_time_overlap(start_time1, end_time1, start_time2, end_time2):
    """Check if two time ranges overlap."""
    # Convert to datetime objects if they are valid
    start1 = time_to_datetime(start_time1)
    end1 = time_to_datetime(end_time1)
    start2 = time_to_datetime(start_time2)
    end2 = time_to_datetime(end_time2)

    # If any time is None, return False as it cannot overlap
    if None in [start1, end1, start2, end2]:
        return False

    # If one course starts before the other ends and ends after the other starts, they overlap
    return (start1 < end2 and end1 > start2)

def course_meets_on_same_day_and_no_overlap(course1, course2):
    """Check if two courses meet on the same day and do not overlap in time."""
    # Check if both courses meet on the same day
    days_course1 = set()
    days_course2 = set()

    if course1['meetsOnMonday']:
        days_course1.add("Monday")
    if course1['meetsOnTuesday']:
        days_course1.add("Tuesday")
    if course1['meetsOnWednesday']:
        days_course1.add("Wednesday")
    if course1['meetsOnThursday']:
        days_course1.add("Thursday")
    if course1['meetsOnFriday']:
        days_course1.add("Friday")
    if course1['meetsOnSaturday']:
        days_course1.add("Saturday")
    if course1['meetsOnSunday']:
        days_course1.add("Sunday")
    
    if course2['meetsOnMonday']:
        days_course2.add("Monday")
    if course2['meetsOnTuesday']:
        days_course2.add("Tuesday")
    if course2['meetsOnWednesday']:
        days_course2.add("Wednesday")
    if course2['meetsOnThursday']:
        days_course2.add("Thursday")
    if course2['meetsOnFriday']:
        days_course2.add("Friday")
    if course2['meetsOnSaturday']:
        days_course2.add("Saturday")
    if course2['meetsOnSunday']:
        days_course2.add("Sunday")
    
    # If they meet on at least one common day, check time overlap
    common_days = days_course1 & days_course2
    if common_days:
        # Check if their meeting times overlap on each common day
        for day in common_days:
            # Get the start and end times for both courses on this day
            start_time1 = course1['startTime']
            end_time1 = course1['endTime']
            start_time2 = course2['startTime']
            end_time2 = course2['endTime']
            
            if check_time_overlap(start_time1, end_time1, start_time2, end_time2):
                return True  # Overlap detected
    
    return False  # No overlap

@bp.route('/courses', methods=('GET', 'POST'))
@login_required
def courses():
    user_id = g.user['id']
    db = get_db()
    cursor = db.cursor()

    cursor.execute("SELECT * FROM profiles WHERE user_id = ?", (user_id,))
    profile = cursor.fetchone()
    
    first_name = profile['first_name']
    num_courses_want = profile['num_courses_want']
    current_year = profile['year']
    current_semester = profile['current_semester']
    concentration1_id = profile['concentration1_id']
    concentration2_id = profile['concentration2_id']
    secondary_id = profile['secondary_id']
    want_gened = profile['want_gened']
    want_9am = profile['want_9am']
    want_grad = profile['want_grad']
    want_conc_req = profile['want_conc_req']

    # Get the names of the concentrations
    cursor.execute("SELECT name FROM concentrations WHERE id = ?", (concentration1_id,))
    concentration1_name = cursor.fetchone()
    concentration1_name = concentration1_name['name'] if concentration1_name else None

    cursor.execute("SELECT name FROM concentrations WHERE id = ?", (concentration2_id,))
    concentration2_name = cursor.fetchone()
    concentration2_name = concentration2_name['name'] if concentration2_name else None

    # Get the name of the secondary concentration if it exists
    cursor.execute("SELECT name FROM secondaries WHERE id = ?", (secondary_id,))
    secondary_name = cursor.fetchone()
    secondary_name = secondary_name['name'] if secondary_name else None

    next_year = current_year + 1

    if current_semester == "Fall":
        next_semester = "Spring"
    else:
        next_semester = "Fall"

    dbsemester = f"{next_semester} {next_year}"

    # Fetch completed course IDs
    cursor.execute("SELECT course_id FROM user_courses WHERE user_id = ?", (user_id,))
    completed_courses_ids = {row['course_id'] for row in cursor.fetchall()}

    # Fetch catalog numbers and subject descriptions for completed courses
    cursor.execute("""
        SELECT c.catalogNumber, c.subjectDescription 
        FROM user_courses uc 
        JOIN courses c ON uc.course_id = c.id 
        WHERE uc.user_id = ?
    """, (user_id,))
    completed_courses_details = [
        {"catalogNumber": row["catalogNumber"], "subjectDescription": row["subjectDescription"]}
        for row in cursor.fetchall()
    ]

    recommended_courses = []
    
    if num_courses_want > 0:
        cursor.execute("SELECT * FROM courses c JOIN meeting_patterns m on c.id = m.course_id WHERE m.startTime IS NOT NULL AND semester = ? GROUP BY c.id", (dbsemester,))
        all_courses = cursor.fetchall()

        random.shuffle(all_courses)

        gened_selected = False

        for course in all_courses:
            course_dict = dict(course)

            if course_dict['id'] in completed_courses_ids:
                continue

            if not want_9am and course_dict['startTime'] == "09:00":
                continue

            if not want_gened and course_dict['subjectDescription'] == "GENED":
                continue

            if not want_grad and course_dict['level'] == "Graduate":
                continue

            course_score = 0
# Boost score if the user hasn't taken any course in their desired concentration
            if course_dict['subjectDescription'] == concentration1_name:
                has_taken_in_concentration = False
                for completedcourse in completed_courses_details:
                    if completedcourse['subjectDescription'] == concentration1_name:
                        has_taken_in_concentration = True
                        break
                if not has_taken_in_concentration:
                    course_score += 100  # Boost for courses in concentration1 if none taken

            if course_dict['subjectDescription'] == concentration2_name:
                has_taken_in_concentration = False
                for completedcourse in completed_courses_details:
                    if completedcourse['subjectDescription'] == concentration2_name:
                        has_taken_in_concentration = True
                        break
                if not has_taken_in_concentration:
                    course_score += 100  # Boost for courses in concentration2 if none taken


            if course_dict['subjectDescription'] == concentration1_name:
                if want_conc_req:
                    course_score += 30
                else:
                    course_score += 20

            if course_dict['subjectDescription'] == concentration2_name:
                if want_conc_req:
                    course_score += 30
                else:
                    course_score += 20

            if course_dict['subjectDescription'] == secondary_name:
                if want_conc_req:
                    course_score += 30
                else:
                    course_score += 20

            # Handling GENED courses:
            if course_dict['subject'] == "GENED":
                if want_gened:
                    if not gened_selected:
                        course_score += 500  # Make GENED more likely to be selected
                        gened_selected = True  # Mark that a GENED course has been selected

            for completedcourse in completed_courses_details:
                if course_dict['subjectDescription'] == completedcourse['subjectDescription']:
                    course_score += 10

                numcourse, lettercourse = parse_course_code(course_dict['catalogNumber'])
                numcomplete, lettercomplete = parse_course_code(completedcourse['catalogNumber'])

                if numcourse != None and numcomplete != None:
                    if lettercourse != None and len(lettercourse) == 1 and lettercomplete != None and len(lettercomplete) == 1:
                        if numcourse == numcomplete and course_dict['subjectDescription'] == completedcourse['subjectDescription'] and (ord(lettercourse) == ord(lettercomplete) + 1):
                            course_score += 400

                    if numcourse > numcomplete and course_dict['subjectDescription'] == completedcourse['subjectDescription']:
                        course_score += 50

                    if numcourse > numcomplete and 10 * numcomplete > numcourse and course_dict['subjectDescription'] == completedcourse['subjectDescription'] and (completedcourse['subjectDescription'] == concentration1_name or completedcourse['subjectDescription'] == concentration2_name):
                        course_score += 200

                    if numcourse == (numcomplete + 1) and (course_dict['subjectDescription'] == completedcourse['subjectDescription']) and (completedcourse['subjectDescription'] == concentration1_name or completedcourse['subjectDescription'] == concentration2_name):
                        course_score += 500

                    if numcourse == (numcomplete + 10) and (course_dict['subjectDescription'] == completedcourse['subjectDescription']) and (completedcourse['subjectDescription'] == concentration1_name or completedcourse['subjectDescription'] == concentration2_name):
                        course_score += 500

                    if numcourse == (numcomplete + 100) and (course_dict['subjectDescription'] == completedcourse['subjectDescription']) and (completedcourse['subjectDescription'] == concentration1_name or completedcourse['subjectDescription'] == concentration2_name):
                        course_score += 500


            course_dict['score'] = course_score

            recommended_courses.append(course_dict)

        # Sort courses by score (highest first)
        recommended_courses.sort(key=lambda x: x['score'], reverse=True)
        
        # Filter out overlapping courses by prioritizing the top courses
        final_courses = []
        for course in recommended_courses:
            add_course = True
            for added_course in final_courses:
                if course_meets_on_same_day_and_no_overlap(course, added_course):
                    add_course = False
                    break
            if add_course:
                final_courses.append(course)

        recommended_courses = final_courses[:num_courses_want]

    return render_template('courses/courses.html', num_courses_want=num_courses_want, recommended_courses=recommended_courses, first_name = first_name)

@bp.route('/search_courses')
def search_courses_route():
    query = request.args.get('query', '')
    if query:
        courses = search_courses(query)
        # Convert list of tuples to list of dictionaries
        course_list = [
            {
                'id': course['id'],
                'title': course['title'],
                'subjectDescription': course['subjectDescription'],
                'catalogNumber': course['catalogNumber'],
                'instructor_name': course['instructor_name']
            }
            for course in courses
        ]
        return jsonify(course_list)
    return jsonify([])
