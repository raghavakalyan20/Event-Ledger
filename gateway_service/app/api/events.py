from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.db.models import Event
from app.schemas.event import EventRequest
from app.services.account_client import apply_transaction

router = APIRouter()


@router.post("/events")
async def create_event(
    request: EventRequest,
    db: Session = Depends(get_db)
):
    existing = db.query(Event).filter(
        Event.event_id == request.eventId
    ).first()

    if existing:
        return {
            "message": "Duplicate event ignored",
            "eventId": existing.event_id
        }

    payload = {
        "eventId": request.eventId,
        "accountId": request.accountId,
        "type": request.type,
        "amount": request.amount,
        "currency": request.currency,
        "eventTimestamp": request.eventTimestamp.isoformat(),
        "metadata": request.metadata
    }

    await apply_transaction(payload)

    event = Event(
        event_id=request.eventId,
        account_id=request.accountId,
        type=request.type,
        amount=request.amount,
        currency=request.currency,
        event_timestamp=request.eventTimestamp,
        event_metadata=request.metadata
    )

    db.add(event)
    db.commit()
    db.refresh(event)

    return {
        "message": "Event created successfully",
        "eventId": event.event_id
    }


@router.get("/events/{event_id}")
def get_event(
    event_id: str,
    db: Session = Depends(get_db)
):
    event = db.query(Event).filter(
        Event.event_id == event_id
    ).first()

    if not event:
        raise HTTPException(
            status_code=404,
            detail="Event not found"
        )

    return event


@router.get("/events")
def list_events(
    account: str,
    db: Session = Depends(get_db)
):
    events = db.query(Event).filter(
        Event.account_id == account
    ).order_by(
        Event.event_timestamp.asc()
    ).all()

    return events