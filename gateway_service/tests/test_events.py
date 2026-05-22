from fastapi.testclient import TestClient
from unittest.mock import patch
from app.main import app

client = TestClient(app)


@patch("app.api.events.apply_transaction")
def test_create_event(mock_apply):
    mock_apply.return_value = {"message": "ok"}

    response = client.post(
        "/events",
        json={
            "eventId": "evt-1",
            "accountId": "acct-1",
            "type": "CREDIT",
            "amount": 100,
            "currency": "USD",
            "eventTimestamp": "2026-05-15T14:02:11Z"
        }
    )

    assert response.status_code == 200
    

@patch("app.api.events.apply_transaction")
def test_duplicate_event(mock_apply):
    mock_apply.return_value = {"message": "ok"}

    payload = {
        "eventId": "evt-dup",
        "accountId": "acct-1",
        "type": "CREDIT",
        "amount": 100,
        "currency": "USD",
        "eventTimestamp": "2026-05-15T14:02:11Z"
    }

    client.post("/events", json=payload)

    response = client.post("/events", json=payload)

    assert response.status_code == 200
    assert response.json()["message"] == "Duplicate event ignored"
    
    
def test_invalid_amount():
    response = client.post(
        "/events",
        json={
            "eventId": "evt-invalid",
            "accountId": "acct-1",
            "type": "CREDIT",
            "amount": -10,
            "currency": "USD",
            "eventTimestamp": "2026-05-15T14:02:11Z"
        }
    )

    assert response.status_code == 422
    

def test_invalid_amount():
    response = client.post(
        "/events",
        json={
            "eventId": "evt-invalid",
            "accountId": "acct-1",
            "type": "CREDIT",
            "amount": -10,
            "currency": "USD",
            "eventTimestamp": "2026-05-15T14:02:11Z"
        }
    )

    assert response.status_code == 422
    

@patch("app.api.events.apply_transaction")
def test_out_of_order_events(mock_apply):
    mock_apply.return_value = {"message": "ok"}

    client.post(
        "/events",
        json={
            "eventId": "evt-10",
            "accountId": "acct-sort",
            "type": "CREDIT",
            "amount": 100,
            "currency": "USD",
            "eventTimestamp": "2026-05-16T14:02:11Z"
        }
    )

    client.post(
        "/events",
        json={
            "eventId": "evt-11",
            "accountId": "acct-sort",
            "type": "CREDIT",
            "amount": 100,
            "currency": "USD",
            "eventTimestamp": "2026-05-15T14:02:11Z"
        }
    )

    response = client.get("/events?account=acct-sort")

    assert response.status_code == 200
    

