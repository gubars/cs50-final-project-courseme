import sqlite3
import json

sqlite_file = r"C:\Users\gubar\cs50-final-project-courseme\instance\courseme.sqlite"

# Open the SQLite database
conn = sqlite3.connect(sqlite_file)
cursor = conn.cursor()

# Load the JSON data
with open('courses-2025.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

# Insert instructors
for course in data:
    for instructor in course.get('instructors', []):  # Default to empty list if no instructors
        cursor.execute("INSERT INTO instructors (name, email) VALUES (?, ?)", (instructor['name'], instructor['email']))
    conn.commit()

# Insert courses
for course in data:
    # Handling the case where instructors might be missing
    instructor_name = course['instructors'][0]['name'] if course.get('instructors') else 'Unknown Instructor'
    cursor.execute("SELECT id FROM instructors WHERE name = ?", (instructor_name,))
    instructor_result = cursor.fetchone()
    instructor_id = instructor_result[0] if instructor_result else None  # Default to None if no instructor found

    cursor.execute('''INSERT INTO courses (title, subject, subjectDescription, catalogNumber, level, academicGroup, semester, academicYear, classSection, component, description, instructor_id) 
                      VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                      (course['title'], course['subject'], course['subjectDescription'], course['catalogNumber'], course['level'], course['academicGroup'],
                       course['semester'], course['academicYear'], course['classSection'], course['component'], course['description'], instructor_id))
    conn.commit()

    # Insert meeting patterns
    cursor.execute("SELECT id FROM courses WHERE title = ?", (course['title'],))
    course_result = cursor.fetchone()
    course_id = course_result[0] if course_result else None  # Default to None if course id is not found
    for meeting in course.get('meetingPatterns', []):  # Default to empty list if no meetingPatterns
        cursor.execute('''INSERT INTO meeting_patterns (course_id, startTime, endTime, startDate, endDate, meetsOnMonday, meetsOnTuesday, meetsOnWednesday, meetsOnThursday, meetsOnFriday, meetsOnSaturday, meetsOnSunday) 
                          VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', 
                          (course_id, meeting['startTime'], meeting['endTime'], meeting['startDate'], meeting['endDate'], meeting['meetsOnMonday'], meeting['meetsOnTuesday'],
                           meeting['meetsOnWednesday'], meeting['meetsOnThursday'], meeting['meetsOnFriday'], meeting['meetsOnSaturday'], meeting['meetsOnSunday']))
    conn.commit()

# Close the connection
conn.close()
