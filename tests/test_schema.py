from src.models.booking import BookingResponse
from src.utils.assert_util import assert_schema, assert_status_code


def test_create_booking_schema(client):
    payload = {
        "firstname": "Schema",
        "lastname": "Test",
        "totalprice": 100,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-03-01", "checkout": "2026-03-05"},
        "additionalneeds": "Dinner",
    }
    resp = client.post("/booking", json=payload)
    assert_status_code(resp, 200)
    assert_schema(resp.json(), BookingResponse)


# def test_create_booking_failed_schema(client):
#     payload = {
#         "firstname": "Schema",
#         "lastname": "Test",
#         "totalprice": 100,
#         "depositpaid": True,
#         "bookingdates": {"checkin": "2026-03-99", "checkout": "2026-03-05"},
#         "additionalneeds": "Dinner",
#     }
#     resp = client.post("/booking", json=payload)
#     assert_status_code(resp, 200)
#     assert_schema(resp.json(), BookingResponse)