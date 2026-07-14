"""Unit tests for logout.py (least-covered module: 0% baseline)."""


def test_logout_clears_session_and_redirects(client):
    with client.session_transaction() as sess:
        sess["logged_in"] = True
        sess["user_type"] = "admin"
        sess["username"] = "alice"

    resp = client.get("/logout")

    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")

    with client.session_transaction() as sess:
        assert "logged_in" not in sess
        assert "user_type" not in sess
        assert "username" not in sess


def test_logout_flashes_success_message(client):
    resp = client.get("/logout", follow_redirects=True)
    assert resp.status_code == 200
    assert b"You have been logged out." in resp.data


def test_logout_when_not_logged_in_still_redirects(client):
    resp = client.get("/logout")
    assert resp.status_code == 302
    assert resp.headers["Location"].endswith("/")
