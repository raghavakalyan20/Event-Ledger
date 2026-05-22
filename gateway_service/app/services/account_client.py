import httpx
from fastapi import HTTPException

ACCOUNT_SERVICE_URL = "http://localhost:8001"


async def apply_transaction(payload: dict):
    try:
        async with httpx.AsyncClient(timeout=5.0) as client:
            response = await client.post(
                f"{ACCOUNT_SERVICE_URL}/accounts/{payload['accountId']}/transactions",
                json=payload
            )

            response.raise_for_status()

            return response.json()

    except httpx.RequestError:
        raise HTTPException(
            status_code=503,
            detail="Account service unavailable"
        )

    except httpx.HTTPStatusError:
        raise HTTPException(
            status_code=503,
            detail="Account service failed"
        )