from sqlalchemy import Column, String, Float, Integer
from .database import Base

class Account(Base):
    __tablename__ = "accounts"

    account_id = Column(String, primary_key=True)
    balance = Column(Float, default=0.0)

class Transaction(Base):
    __tablename__ = "transactions"

    id = Column(Integer, primary_key=True)
    event_id = Column(String, unique=True)
    account_id = Column(String)
    type = Column(String)
    amount = Column(Float)