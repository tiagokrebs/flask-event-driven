import sqlite3
import click
from flask import current_app, g

# flask --app app init-db
# flask --app app run

# register db with the app
def init_app(app):
    # teardowen closes the connection at the end of the request
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)

# get the db connection
def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# close the db connection
def close_db(e=None):
    db = g.pop('db', None)
    if db is not None:
        db.close()

# init the db
def init_db():
    db = get_db()
    # could be a simple file read instead current_app.open_resource
    with current_app.open_resource('schema.sql') as f:
        db.executescript(f.read().decode('utf8'))

# CLI decorator
@click.command('init-db')
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo('Initialized the database.')
