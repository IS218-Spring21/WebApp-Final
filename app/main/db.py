"""
Database for users
"""
# http://flask.pocoo.org/docs/1.0/tutorial/database/
import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext


def get_db():
    """
    Gets the users db
    :return: users database
    """
    if "db" not in g:
        g.db = sqlite3.connect(
            "sqlite_db", detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db


def close_db():
    """
    Closes the DB
    There was a param e=None
    :return: closes the DB
    """
    db_ = g.pop("db", None)

    if db_ is not None:
        db_.close()


def init_db():
    """
    Initializes the DB
    :return: Initializes the DB
    """
    db_ = get_db()

    with current_app.open_resource("usersDB.sql") as sql_file:
        db_.executescript(sql_file.read().decode("utf8"))


@click.command("init-db")
@with_appcontext
def init_db_command():
    """Clear the existing data and create new tables."""
    init_db()
    click.echo("Initialized the database.")


def init_app(app):
    """
    :param app: name of the app
    :return: initializes the app DB
    """
    app.teardown_appcontext(close_db)
    app.cli.add_command(init_db_command)
