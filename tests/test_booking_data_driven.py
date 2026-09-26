import pytest


from src.utils.data_loader import load_yaml


CASES = load_yaml("booking_cases.yaml")["create_booking"]


@pytest.mark.parametrize("case", CASES, ids=[c["case"] for c in CASES])
def test_create_booking_data_driven(client, case):
    expected = case["expected_status"]
    retry = 0 if expected >= 400 else None
    resp = client.post("/booking", json=case["payload"], retry=retry)
    assert resp.status_code == expected, (
        f"case={case['case']}, status={resp.status_code}, body={resp.text}"
    )
