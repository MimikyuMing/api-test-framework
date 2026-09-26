def test_ping(client):
    resp = client.get("/ping")
    assert resp.status_code == 201

def test_get_booking_ids(client):
    resp = client.get("/booking")
    assert resp.status_code == 200
    assert isinstance(resp.json(), list)