import requests


def test_gateway_to_account_integration():
    payload = {
        "eventId": "evt-int",
        "accountId": "acct-int",
        "type": "CREDIT",
        "amount": 100,
        "currency": "USD",
        "eventTimestamp": "2026-05-15T14:02:11Z"
    }

    response = requests.post(
        "http://localhost:8000/events",
        json=payload
    )

    assert response.status_code == 200

    balance = requests.get(
        "http://localhost:8001/accounts/acct-int/balance"
    )

    assert balance.status_code == 200
    assert balance.json()["balance"] == 100