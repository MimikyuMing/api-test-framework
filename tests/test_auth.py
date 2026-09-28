from src.utils.assert_util import assert_field, assert_status_code


def test_login_success(client, config):
    resp = client.post("/auth", json=config["auth"])
    assert resp.status_code == 200
    assert_status_code(resp, 200)
    assert "token" in resp.json()


def test_login_wrong_password(client, config):
    payload = {
        "username": config["auth"]["username"],
        "password": "wrong_password",
    }
    resp = client.post("/auth", json=payload)
    assert_status_code(resp, 200)
    assert_field(resp.json(), "reason", "Bad credentials")