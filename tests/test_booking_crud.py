import pytest


@pytest.fixture(scope="function")
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
    assert resp.status_code == 200
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
    assert resp.status_code == 200
    data = resp.json()
    assert "bookingid" in data
    assert data["booking"]["firstname"] == "Jim"


def test_get_booking(client, new_booking):
    booking_id, _ = new_booking
    resp = client.get(f"/booking/{booking_id}")
    assert resp.status_code == 200
    assert resp.json()["firstname"] == "Jim"


def test_update_booking(client, auth_headers, new_booking):
    booking_id, payload = new_booking
    payload['firstname'] = "Updated"
    resp = client.put(
        f"/booking/{booking_id}",
        json=payload,
        headers=auth_headers
    )
    assert resp.status_code == 200
    assert resp.json()["firstname"] == "Updated"


def test_delete_booking(client, auth_headers, new_booking):
    booking_id, _ = new_booking
    resp = client.delete(f"/booking/{booking_id}", headers=auth_headers)
    assert resp.status_code in (200, 201), f"意外状态码: {resp.status_code}"


def test_get_deleted_booking(client, new_booking, auth_headers):
    booking_id, _ = new_booking
    client.delete(f"/booking/{booking_id}", headers=auth_headers)
    resp = client.get(f"/booking/{booking_id}")
    assert resp.status_code == 404