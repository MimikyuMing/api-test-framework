from src.utils.assert_util import assert_field, assert_status_code


def test_full_crud_flow(client, auth_headers):
    payload = {
        "firstname": "Flow",
        "lastname": "Test",
        "totalprice": 200,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-02-01", "checkout": "2026-02-05"},
        "additionalneeds": "Lunch",
    }

    # 1. 创建
    create_resp = client.post("/booking", json=payload)
    assert_status_code(create_resp, 200)
    booking_id = create_resp.json()["bookingid"]
    assert booking_id > 0

    # 2. 查询
    get_resp = client.get(f"/booking/{booking_id}")
    assert_status_code(get_resp, 200)
    assert_field(get_resp.json(), "firstname", "Flow")

    # 3. 更新
    payload["firstname"] = "Updated"
    put_resp = client.put(
        f"/booking/{booking_id}", json=payload, headers=auth_headers
    )
    assert_status_code(put_resp, 200)
    assert_field(put_resp.json(), "firstname", "Updated")

    # 4. 删除
    del_resp = client.delete(f"/booking/{booking_id}", headers=auth_headers)
    assert del_resp.status_code in (200, 201), f"删除异常: {del_resp.status_code}"

    # 5. 确认已删除
    final_resp = client.get(f"/booking/{booking_id}")
    assert_status_code(final_resp, 404)