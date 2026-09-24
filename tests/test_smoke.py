import requests

BASE_URL = "https://restful-booker.herokuapp.com"

def test_ping():
    resp = requests.get(f"{BASE_URL}/ping")
    assert resp.status_code == 201

def test_get_booking_ids():
    resp = requests.get(f"{BASE_URL}/booking")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)