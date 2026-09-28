import pytest


from src.utils.data_loader import load_yaml
from src.utils.assert_util import assert_status_code


CASES = load_yaml("booking_cases.yaml")["create_booking"]


@pytest.mark.parametrize("case", CASES, ids=[c["case"] for c in CASES])
def test_create_booking_data_driven(client, case):
    expected = case["expected_status"]
    retry = 0 if expected >= 400 else None
    resp = client.post("/booking", json=case["payload"], retry=retry)
    assert_status_code(resp, case["expected_status"])
