import sqlite3
from datetime import datetime

import click
from flask import current_app, g

# References
# - Used Flask documentation to get webpage setup, https://flask.palletsprojects.com/en/stable/tutorial/

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        # Allows us to access the columns by name
        g.db.row_factory = sqlite3.Row

    return g.db

# Checks if g.db was set
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    # Returns database connection
    db = get_db()

    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# Calls the init_db function and shows success message to user
@click.command('init-db')
def init_db_command():
    init_db()
    click.echo('Initialized the database.')

sqlite3.register_converter(
    "timestamp", lambda v: datetime.fromisoformat(v.decode())
)

def init_app(app):
    # Calls close_db when cleaning up
    app.teardown_appcontext(close_db)
    # Adds init_db_command that can be called with flask
    app.cli.add_command(init_db_command)

def search_courses(query):
    db = get_db()
    query = query.strip()  # Remove leading/trailing whitespace
    query_parts = query.split()  # Split query into parts (e.g., "Physics 16")
    
    # Build SQL query for flexible matching
    sql = '''
        SELECT courses.id, courses.title, courses.catalogNumber, courses.subjectDescription, instructors.name AS instructor_name
        FROM courses
        LEFT JOIN instructors ON courses.instructor_id = instructors.id
        WHERE
            LOWER(courses.title) LIKE ? OR
            LOWER(courses.subjectDescription) LIKE ? OR
            LOWER(courses.catalogNumber) LIKE ?
    '''
    
    # If query has two parts, attempt to match subject and catalogNumber together
    params = [f"%{query}%", f"%{query}%", f"%{query}%"]  # Default single-part query handling
    if len(query_parts) == 2:  # If the query has two parts, assume subject + catalogNumber
        subject_part, catalog_part = query_parts
        sql += ' OR (LOWER(courses.subjectDescription) = ? AND LOWER(courses.catalogNumber) = ?)'
        params.extend([subject_part.lower(), catalog_part.lower()])
    
    sql += ' LIMIT 5'  # Limit results to 5
    
    # Execute query
    cursor = db.execute(sql, params)
    courses = cursor.fetchall()
    return courses