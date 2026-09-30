import allure
import pytest

from src.models.booking import BookingResponse
from src.utils.assert_util import assert_field, assert_schema, assert_status_code


@pytest.fixture
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
    assert_status_code(resp, 200)
    booking_id = resp.json()["bookingid"]
    yield booking_id, payload

@allure.feature("Booking")
@allure.story("Create")
@allure.title("创建 booking - 正常参数")
def test_create_booking(client):
    with allure.step("准备请求数据"):
        payload = {
            "firstname": "Jim",
            "lastname": "Brown",
            "totalprice": 111,
            "depositpaid": True,
            "bookingdates": {"checkin": "2026-01-01", "checkout": "2026-01-05"},
            "additionalneeds": "Breakfast",
        }
    with allure.step("发送 POST /booking"):
        resp = client.post("/booking", json=payload)
    with allure.step("校验状态码 200"):
        assert_status_code(resp, 200)

    with allure.step("校验响应结构"):
        assert_schema(resp.json(), BookingResponse)

    with allure.step("校验 firstname 字段"):
        assert_field(resp.json()["booking"], "firstname", "Jim")


@allure.feature("Booking")
@allure.story("Read")
@allure.title("查询 booking")
def test_get_booking(client, new_booking):
    booking_id, _ = new_booking
    with allure.step(f"发送 GET /booking/{booking_id}"):
        resp = client.get(f"/booking/{booking_id}")
    with allure.step("校验状态码 200"):
        assert_status_code(resp, 200)
    with allure.step("校验 firstname 字段"):
        assert_field(resp.json(), "firstname", "Jim")


@allure.feature("Booking")
@allure.story("Update")
@allure.title("更新 booking")
def test_update_booking(client, auth_headers, new_booking):
    booking_id, payload = new_booking
    payload["firstname"] = "Updated"
    with allure.step(f"发送 PUT /booking/{booking_id}"):
        resp = client.put(
            f"/booking/{booking_id}", json=payload, headers=auth_headers
        )
    with allure.step("校验状态码 200"):
        assert_status_code(resp, 200)
    with allure.step("校验 firstname 已更新"):
        assert_field(resp.json(), "firstname", "Updated")


@allure.feature("Booking")
@allure.story("Delete")
@allure.title("删除 booking")
def test_delete_booking(client, auth_headers, new_booking):
    booking_id, _ = new_booking
    with allure.step(f"发送 DELETE /booking/{booking_id}"):
        client.delete(f"/booking/{booking_id}", headers=auth_headers)
    with allure.step("确认已删除，GET 返回 404"):
        resp = client.get(f"/booking/{booking_id}")
        assert_status_code(resp, 404)