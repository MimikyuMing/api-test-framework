import allure

from src.utils.assert_util import assert_status_code


@allure.feature("Demo")
@allure.story("Smoke")
@allure.title("健康检查")
@allure.severity(allure.severity_level.CRITICAL)
def test_ping_with_allure(client):
    with allure.step("发送 GET /ping"):
        resp = client.get("/ping")

    with allure.step("校验状态码 201"):
        assert_status_code(resp, 201)