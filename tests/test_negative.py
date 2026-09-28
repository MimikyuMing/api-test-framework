import pytest

from src.utils.assert_util import assert_field, assert_status_code


def test_login_wrong_password(client, config):
    payload = {
        "username": config["auth"]["username"],
        "password": "wrong_password",
    }
    resp = client.post("/auth", json=payload)
    assert_status_code(resp, 200)
    assert_field(resp.json(), "reason", "Bad credentials")


def test_get_nonexistent_booking(client):
    resp = client.get("/booking/99999999")
    assert_status_code(resp, 404)


def test_update_without_token(client, new_booking_for_negative):
    booking_id, payload = new_booking_for_negative
    resp = client.put(f"/booking/{booking_id}", json=payload)
    assert_status_code(resp, 403)


def test_create_missing_firstname(client):
    payload = {
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
    }
    resp = client.post("/booking", json=payload, retry=0)
    assert_status_code(resp, 500)


@pytest.mark.parametrize("price", [0, -1, 999999])
def test_create_price_boundary(client, price):
    payload = {
        "firstname": "Edge",
        "lastname": "Test",
        "totalprice": price,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
    }
    resp = client.post("/booking", json=payload)
    assert_status_code(resp, 200)


def test_create_reversed_dates(client):
    payload = {
        "firstname": "Edge",
        "lastname": "Test",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-05", "checkout": "2026-01-01"},
    }
    resp = client.post("/booking", json=payload)
    assert_status_code(resp, 200)