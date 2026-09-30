def assert_status_code(resp, expected):
    """断言响应状态码。

    Args:
        resp: requests.Response 对象。
        expected: 期望的状态码。
    """
    assert resp.status_code == expected, (
        f"expected status {expected}, got {resp.status_code}, "
        f"body={resp.text}"
    )


def assert_field(data, field, expected):
    """断言字典中某个字段的值。

    Args:
        data: 字典，如 resp.json()。
        field: 字段名。
        expected: 期望值。
    """
    actual = data.get(field)
    assert actual == expected, (
        f"field '{field}': expected {expected}, got {actual}"
    )


def assert_fields(data, expected_dict):
    """批量断言多个字段。

    Args:
        data: 字典。
        expected_dict: {字段名: 期望值} 的字典。
    """
    for field, expected in expected_dict.items():
        assert_field(data, field, expected)


from pydantic import ValidationError


def assert_schema(data, model_cls):
    """用 pydantic 模型校验数据结构。

    Args:
        data: 字典。
        model_cls: pydantic BaseModel 子类。
    """
    try:
        model_cls(**data)
    except (ValidationError, TypeError) as e:
        raise AssertionError(f"schema validation failed: {e}")