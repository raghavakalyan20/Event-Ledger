from pydantic import BaseModel, Field
from enum import Enum
from typing import Optional, Dict
from datetime import datetime


class EventType(str, Enum):
    CREDIT = "CREDIT"
    DEBIT = "DEBIT"


class EventRequest(BaseModel):
    eventId: str
    accountId: str
    type: EventType
    amount: float = Field(gt=0)
    currency: str
    eventTimestamp: datetime
    metadata: Optional[Dict] = None