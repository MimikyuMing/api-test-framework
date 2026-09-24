import pytest


from src.client.http_client import HttpClient
from src.utils.config_loader import load_config



@pytest.fixture(scope="session")
def client():
    config = load_config()
    return HttpClient(config["base_url"], config["timeout"], config["retry"])


def test_ping(client):
    resp = client.get("/ping")
    assert resp.status_code == 201

def test_get_booking_ids(client):
    resp = client.get("/booking")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)