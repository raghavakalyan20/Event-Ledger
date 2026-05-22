from pydantic import BaseModel
from enum import Enum
from datetime import datetime


class TransactionType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class TransactionRequest(BaseModel):
    eventId: str
    accountId: str
    type: TransactionType
    amount: float
    currency: str
    eventTimestamp: datetime