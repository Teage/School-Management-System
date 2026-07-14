import os
import sqlite3
import sys
import tempfile

import pytest

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if ROOT not in sys.path:
    sys.path.insert(0, ROOT)

import hello  # noqa: E402


@pytest.fixture
def db_path(monkeypatch):
    """Redirect the app's sqlite connections to a throwaway database.

    hello.py hardcodes ``sqlite3.connect('users.db')``; the real ``users.db``
    is tracked in git, so tests must never touch it.
    """
    fd, path = tempfile.mkstemp(suffix=".db")
    os.close(fd)

    real_connect = sqlite3.connect

    def fake_connect(_database, *args, **kwargs):
        return real_connect(path, *args, **kwargs)

    monkeypatch.setattr(hello.sqlite3, "connect", fake_connect)
    hello.init_db()  # create the LoginDetails table in the temp db
    try:
        yield path
    finally:
        os.remove(path)


@pytest.fixture
def app(db_path):
    hello.app.config.update(TESTING=True, WTF_CSRF_ENABLED=False)
    return hello.app


@pytest.fixture
def client(app):
    return app.test_client()


def seed_user(db_path, email="a@b.com", username="alice",
              password="secret", user_type="admin"):
    """Insert a user with a properly hashed password into the temp db."""
    from werkzeug.security import generate_password_hash

    conn = sqlite3.connect(db_path)
    conn.execute(
        "INSERT INTO LoginDetails (email, username, password, user_type) "
        "VALUES (?, ?, ?, ?)",
        (email, username, generate_password_hash(password), user_type),
    )
    conn.commit()
    conn.close()
