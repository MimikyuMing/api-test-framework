import requests

BASE_URL = "https://restful-booker.herokuapp.com"

# 1. totalprice 为负数
payload = {
    "firstname": "Edge",
    "lastname": "Test",
    "totalprice": -1,
    "depositpaid": True,
    "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
}
resp = requests.post(f"{BASE_URL}/booking", json=payload)
print("negative price:", resp.status_code, resp.text[:200])

# 2. checkin 晚于 checkout
payload["totalprice"] = 100
payload["bookingdates"] = {"checkin": "2026-01-05", "checkout": "2026-01-01"}
resp = requests.post(f"{BASE_URL}/booking", json=payload)
print("reversed dates:", resp.status_code, resp.text[:200])