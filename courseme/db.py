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