import pytest

from src.models.booking import BookingResponse
from src.utils.assert_util import assert_field, assert_status_code, assert_schema


@pytest.fixture
def new_booking(client):
    payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
        "additionalneeds": "Breakfast",
    }
    resp = client.post("/booking", json=payload)
    assert_status_code(resp, 200)
    booking_id = resp.json()["bookingid"]
    yield booking_id, payload


def test_create_booking(client):
    payload = {
        "firstname": "Jim",
        "lastname": "Brown",
        "totalprice": 111,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
        "additionalneeds": "Breakfast",
    }
    resp = client.post("/booking", json=payload)
    assert_status_code(resp, 200)
    assert_schema(resp.json(), BookingResponse)
    assert_field(resp.json()["booking"], "firstname", "Jim")


def test_get_booking(client, new_booking):
    booking_id, _ = new_booking
    resp = client.get(f"/booking/{booking_id}")
    assert_status_code(resp, 200)
    assert_field(resp.json(), "firstname", "Jim")


def test_update_booking(client, auth_headers, new_booking):
    booking_id, payload = new_booking
    payload["firstname"] = "Updated"
    resp = client.put(
        f"/booking/{booking_id}", json=payload, headers=auth_headers
    )
    assert_status_code(resp, 200)
    assert_field(resp.json(), "firstname", "Updated")


def test_delete_booking(client, auth_headers, new_booking):
    booking_id, _ = new_booking
    client.delete(f"/booking/{booking_id}", headers=auth_headers)
    resp = client.get(f"/booking/{booking_id}")
    assert_status_code(resp, 404)