# Event Ledger

This project is a simple event ledger system built as a take-home exercise using a microservices approach.

It consists of two services:

- **Gateway Service** – public-facing API that receives transaction events
- **Account Service** – internal service responsible for account balances and transaction history

## Architecture Overview

The Gateway Service accepts incoming events, validates them, checks for duplicate submissions using `eventId`, stores the event locally, and forwards valid transactions to the Account Service.

The Account Service applies the transaction to the account, maintains the balance, and stores transaction history.

Both services are independent and use separate SQLite databases.

Architecture flow:

```text
Client
   |
   v
Gateway Service
(FastAPI + SQLite)
   |
   v
Account Service
(FastAPI + SQLite)
```

---

## Setup Instructions

### Prerequisites

Make sure the following are installed:

- Python 3.11+
- pip
- Docker
- Docker Compose

---

## Install Dependencies

### Gateway Service

```bash
cd gateway_service
pip install -r requirements.txt
```

### Account Service

```bash
cd account_service
pip install -r requirements.txt
```

---

## Running the Services

### Option 1: Docker Compose

From the project root:

```bash
docker compose build
docker compose up
```

Services will be available at:

Gateway:

```bash
http://localhost:8000/docs
```

Account Service:

```bash
http://localhost:8001/docs
```

---

### Option 2: Run Manually

Start Account Service:

```bash
cd account_service
uvicorn app.main:app --reload --port 8001
```

Start Gateway Service:

```bash
cd gateway_service
uvicorn app.main:app --reload --port 8000
```

---

## Running Tests

### Gateway Tests

```bash
cd gateway_service
pytest
```

### Account Service Tests

```bash
cd account_service
pytest
```

---

## Resiliency Approach

The Gateway Service uses timeout-based failure handling when calling the Account Service.

If the Account Service is unavailable or does not respond in time, the Gateway returns:

```http
503 Service Unavailable
```

instead of hanging or returning an unclear server error.

This keeps failure behavior predictable and allows event lookup endpoints to continue functioning even if the downstream service is unavailable.