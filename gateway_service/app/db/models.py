from sqlalchemy import Column, String, Float, DateTime, JSON
from app.db.database import Base


class Event(Base):
    __tablename__ = "events"

    event_id = Column(String, primary_key=True, index=True)
    account_id = Column(String, nullable=False, index=True)
    type = Column(String, nullable=False)
    amount = Column(Float, nullable=False)
    currency = Column(String, nullable=False)
    event_timestamp = Column(DateTime, nullable=False)
    event_metadata = Column(JSON, nullable=True)