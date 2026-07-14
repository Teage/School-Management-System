"""Unit tests for hello.py (0% baseline coverage)."""

import sqlite3

from tests.conftest import seed_user


def login(client, username, user_type, password):
    return client.post(
        "/validate_login",
        data={"username": username, "user": user_type, "password": password},
    )


# --- public pages -----------------------------------------------------------

def test_login_page_renders(client):
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"<form" in resp.data.lower()


def test_register_page_renders(client):
    resp = client.get("/register")
    assert resp.status_code == 200


def test_blog_page_returns_post_id(client):
    resp = client.get("/blog/42")
    assert resp.status_code == 200
    assert b"blog post number 42" in resp.data


def test_blog_page_rejects_non_integer(client):
    assert client.get("/blog/abc").status_code == 404


# --- access-control decorators ----------------------------------------------

def test_admin_requires_login_redirects(client):
    resp = client.get("/admin")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")


def test_user_requires_login_redirects(client):
    resp = client.get("/user")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")


def test_admin_forbidden_for_user_role(client):
    with client.session_transaction() as sess:
        sess["logged_in"] = True
        sess["user_type"] = "user"
        sess["user_id"] = 1
    resp = client.get("/admin")
    assert resp.status_code == 302


def test_admin_accessible_for_admin_role(client):
    with client.session_transaction() as sess:
        sess["logged_in"] = True
        sess["user_type"] = "admin"
        sess["user_id"] = 1
        sess["username"] = "alice"
    resp = client.get("/admin")
    assert resp.status_code == 200


def test_user_accessible_for_user_role(client):
    with client.session_transaction() as sess:
        sess["logged_in"] = True
        sess["user_type"] = "user"
        sess["user_id"] = 1
        sess["username"] = "bob"
    resp = client.get("/user")
    assert resp.status_code == 200


# --- registration ------------------------------------------------------------

def test_register_creates_user(client, db_path):
    resp = client.post(
        "/register",
        data={
            "email": "new@example.com",
            "username": "newuser",
            "user": "user",
            "password": "pw",
            "confirm_password": "pw",
        },
    )
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")

    conn = sqlite3.connect(db_path)
    row = conn.execute(
        "SELECT username, user_type FROM LoginDetails WHERE email = ?",
        ("new@example.com",),
    ).fetchone()
    conn.close()
    assert row == ("newuser", "user")


def test_register_hashes_password(client, db_path):
    client.post(
        "/register",
        data={
            "email": "h@example.com",
            "username": "hashuser",
            "user": "user",
            "password": "plaintext",
            "confirm_password": "plaintext",
        },
    )
    conn = sqlite3.connect(db_path)
    stored = conn.execute(
        "SELECT password FROM LoginDetails WHERE email = ?", ("h@example.com",)
    ).fetchone()[0]
    conn.close()
    assert stored != "plaintext"


def test_register_flashes_on_password_mismatch(client, db_path):
    resp = client.post(
        "/register",
        data={
            "email": "mismatch@example.com",
            "username": "mm",
            "user": "user",
            "password": "one",
            "confirm_password": "two",
        },
        follow_redirects=True,
    )
    assert b"Passwords do not match." in resp.data


def test_register_rejects_duplicate_email(client, db_path):
    seed_user(db_path, email="dupe@example.com", username="orig")
    resp = client.post(
        "/register",
        data={
            "email": "dupe@example.com",
            "username": "someoneelse",
            "user": "user",
            "password": "pw",
            "confirm_password": "pw",
        },
    )
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/register")


# --- login validation --------------------------------------------------------

def test_validate_login_success_admin_sets_session(client, db_path):
    seed_user(db_path, username="admin1", password="pw", user_type="admin")
    resp = login(client, "admin1", "admin", "pw")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/admin")
    with client.session_transaction() as sess:
        assert sess["logged_in"] is True
        assert sess["username"] == "admin1"
        assert sess["user_type"] == "admin"


def test_validate_login_success_user_redirects_to_user(client, db_path):
    seed_user(db_path, email="u@e.com", username="user1",
              password="pw", user_type="user")
    resp = login(client, "user1", "user", "pw")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/user")


def test_validate_login_wrong_password_redirects_to_login(client, db_path):
    seed_user(db_path, username="admin1", password="right", user_type="admin")
    resp = login(client, "admin1", "admin", "wrong")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
    with client.session_transaction() as sess:
        assert "logged_in" not in sess


def test_validate_login_unknown_user_redirects_to_login(client, db_path):
    resp = login(client, "ghost", "admin", "pw")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
