def test_full_crud_flow(client, auth_headers):
    payload = {
        "firstname": "Flow",
        "lastname": "Test",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-02-01", "checkout": "2026-02-05"},
        "additionalneeds": "Lunch",
    }

    # 1. create
    create_resp = client.post("/booking", headers=auth_headers, json=payload)
    assert create_resp.status_code == 200, f"创建失败: {create_resp.text}"
    booking_id = create_resp.json()["bookingid"]
    assert booking_id > 0

    # 2. get
    get_resp = client.get(f"/booking/{booking_id}")
    assert get_resp.status_code == 200
    assert get_resp.json()["firstname"] == "Flow"

    # 3. update
    payload["firstname"] = "Updated"
    update_resp = client.put(f"/booking/{booking_id}", headers=auth_headers, json=payload)
    assert update_resp.status_code == 200
    assert update_resp.json()["firstname"] == "Updated"

    # 4. delete
    delete_resp = client.delete(f"/booking/{booking_id}", headers=auth_headers)
    assert delete_resp.status_code in (200,201), f"删除异常: {delete_resp.status_code}"

    # 5. get_deleted
    get_del_resp = client.get(f"/booking/{booking_id}")
    assert get_del_resp.status_code == 404
