from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)


def test_credit_transaction():
    response = client.post(
        "/accounts/acct-1/transactions",
        json={
            "eventId": "evt-100",
            "accountId": "acct-1",
            "type": "CREDIT",
            "amount": 100,
            "currency": "USD",
            "eventTimestamp": "2026-05-15T14:02:11Z"
        }
    )

    assert response.status_code == 200
    assert response.json()["balance"] == 100


def test_debit_transaction():
    response = client.post(
        "/accounts/acct-1/transactions",
        json={
            "eventId": "evt-101",
            "accountId": "acct-1",
            "type": "DEBIT",
            "amount": 40,
            "currency": "USD",
            "eventTimestamp": "2026-05-15T14:02:11Z"
        }
    )

    assert response.status_code == 200
    assert response.json()["balance"] == 60


def test_duplicate_transaction():
    payload = {
        "eventId": "evt-200",
        "accountId": "acct-2",
        "type": "CREDIT",
        "amount": 50,
        "currency": "USD",
        "eventTimestamp": "2026-05-15T14:02:11Z"
    }

    client.post("/accounts/acct-2/transactions", json=payload)

    response = client.post("/accounts/acct-2/transactions", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Duplicate transaction ignored"


def test_balance_lookup():
    response = client.get("/accounts/acct-1/balance")

    assert response.status_code == 200