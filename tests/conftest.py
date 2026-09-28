import pytest

from src.client.http_client import HttpClient
from src.utils.config_loader import load_config


@pytest.fixture(scope="session")
def config():
    return load_config()


@pytest.fixture(scope="session")
def client(config):
    return HttpClient(
        config["base_url"],
        config["timeout"],
        config["retry"],
    )


@pytest.fixture(scope="session")
def auth_token(client, config):
    resp = client.post("/auth", json=config["auth"])
    assert resp.status_code == 200, f"登录失败: {resp.text}"
    return resp.json()["token"]


@pytest.fixture(scope="session")
def auth_headers(auth_token):
    return {"Cookie": f"token={auth_token}"}


@pytest.fixture
def new_booking_for_negative(client):
    payload = {
        "firstname": "Neg",
        "lastname": "Test",
        "totalprice": 50,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
    }
    resp = client.post("/booking", json=payload)
    assert resp.status_code == 200
    booking_id = resp.json()["bookingid"]
    yield booking_id, payload