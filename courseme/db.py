import sqlite3
from datetime import datetime

import click
# g stores data that can be accessed during the request
from flask import current_app, g

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