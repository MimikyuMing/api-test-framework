from src.utils.assert_util import assert_status_code


def test_ping(client):
    resp = client.get("/ping")
    assert_status_code(resp, 201)
    

def test_get_booking_ids(client):
    resp = client.get("/booking")
    assert_status_code(resp, 200)
    assert isinstance(resp.json(), list)