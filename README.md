# Event Ledger

Event Ledger is a simple distributed microservices-based application built to process financial transaction events while handling duplicate requests, out-of-order event delivery, and downstream service failures.

## Approach Followed

The implementation was designed using a simple two-service architecture to maintain clear separation of responsibilities.

### Event Gateway Service
The Gateway acts as the public-facing entry point for all incoming requests.

Responsibilities:
- Accept transaction events
- Validate request payloads
- Enforce idempotency using `eventId`
- Store event records locally
- Forward valid transactions to the Account Service
- Serve event lookup APIs
- Handle Account Service failures gracefully

### Account Service
The Account Service manages account state.

Responsibilities:
- Maintain account balances
- Store transaction history
- Prevent duplicate transaction application
- Serve account-level queries

---

## Architecture

```text
Client
   |
   v
+----------------------+
|  Event Gateway API   |
|   FastAPI + SQLite   |
+----------------------+
          |
          | REST API Call
          v
+----------------------+
|   Account Service    |
|   FastAPI + SQLite   |
+----------------------+
```

---

## Design Decisions

### Independent Services
Both services run independently and maintain separate SQLite databases.

This ensures:
- no shared application state
- clean service boundaries
- easier failure isolation

---

### Idempotency
Duplicate event submissions are handled using `eventId`.

If the same event is submitted multiple times:
- the duplicate is detected
- the event is not processed again
- balance remains unchanged

---

### Out-of-Order Event Handling
Since upstream systems may send events out of sequence, events are stored independently and event listing APIs return results ordered by `eventTimestamp`.

Balance calculations remain correct regardless of arrival order.

---

### Graceful Failure Handling
If the Account Service is unavailable:
- Gateway returns `503 Service Unavailable`
- Event retrieval endpoints continue to work
- Requests do not hang indefinitely

---

## Tech Stack

- Python 3.11
- FastAPI
- SQLAlchemy
- SQLite
- HTTPX
- Docker
- Docker Compose

---

## Running the Application

### Using Docker

From project root:

```bash
docker compose build
docker compose up
```

Gateway:

```bash
http://localhost:8000/docs
```

Account Service:

```bash
http://localhost:8001/docs
```

---

### Running Locally

Start Account Service:

```bash
cd account_service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8001
```

Start Gateway Service:

```bash
cd gateway_service
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

---

## Available APIs

### Gateway
- `POST /events`
- `GET /events/{eventId}`
- `GET /events?account={accountId}`
- `GET /health`

### Account Service
- `POST /accounts/{accountId}/transactions`
- `GET /accounts/{accountId}/balance`
- `GET /accounts/{accountId}`
- `GET /health`

---

## Notes

This implementation focuses on correctness, simplicity, and clear service separation while meeting the core requirements of the exercise.