"""Search model (database) API."""
import sqlite3
import flask
import search


def dict_factory(cursor, row):
    """Return information.

    This takes in two parameters.
    """
    return {col[0]: row[idx] for idx, col in enumerate(cursor.description)}


def get_db():
    """Return information.

    This takes in two parameters.
    """
    if 'sqlite_db' not in flask.g:
        db_filename = search.app.config['DATABASE_FILENAME']
        flask.g.sqlite_db = sqlite3.connect(str(db_filename))
        flask.g.sqlite_db.row_factory = dict_factory
        # Foreign keys have to be enabled per-connection.  This is an sqlite3
        # backwards compatibility thing.
        flask.g.sqlite_db.execute("PRAGMA foreign_keys = ON")
    return flask.g.sqlite_db


@search.app.teardown_appcontext
def close_db(error):
    """Return information.

    This takes in two parameters.
    """
    assert error or not error  # Needed to avoid superfluous style error
    sqlite_db = flask.g.pop('sqlite_db', None)
    if sqlite_db is not None:
        sqlite_db.commit()
        sqlite_db.close()
