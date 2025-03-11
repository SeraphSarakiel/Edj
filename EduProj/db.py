import sqlite3
from datetime import datetime

import click
from flask import current_app, g

def make_dicts(cursor, row):
    return dict((cursor.description[idx][0], value)
                for idx, value in enumerate(row))

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config["DATABASE"],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row #make_dicts #rows like dict

    return g.db

def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()

def init_db():
    db = get_db()
     
    with current_app.open_resource("Schemas/schema.sql") as f:
        db.executescript(f.read().decode("utf8"))

@click.command('init-db')
def init_db_command():
    """ Clear existing data and create new tables"""
    init_db()
    click.echo("Initialized the database")

sqlite3.register_converter(
    "timestamp", lambda v:datetime.fromisoformat(v.decode())
)

@click.command('populate-testdata')
def populate_testdata():
    """Create test data in predefined Tables"""
    db = get_db()
    with current_app.open_resource("Schemas/testData.sql") as f:
        db.executescript(f.read().decode("utf8"))
    click.echo("Database is now populated with test data")

def init_app(app):
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
    app.cli.add_command(populate_testdata)

