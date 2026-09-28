def assert_status_code(resp, expected):
    assert resp.status_code == expected, (
        f"expected status {expected}, got {resp.status_code}, "
        f"body={resp.text}"
    )

def assert_field(data, field, expected):
    actual = data.get(field)
    assert actual == expected, (
        f"field '{field}': expected {expected}, got {actual}"
    )

def assert_fields(data, expected_dict):
    for field, expected in expected_dict.items():
        assert_field(data, field, expected)

def assert_schema(data, model_cls):
    try:
        model_cls(**data)
    except Exception as e:
        raise AssertionError(f"schema validation failed: {e}")