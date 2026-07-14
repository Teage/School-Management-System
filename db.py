from contextlib import contextmanager

import sqlite3

DATABASE = "users.db"


@contextmanager
def get_db():
    """Yield a SQLite connection, committing on success and always closing."""
    connection = sqlite3.connect(DATABASE)
    try:
        yield connection
        connection.commit()
    finally:
        connection.close()
