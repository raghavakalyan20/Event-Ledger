from fastapi import FastAPI
from app.api import accounts
from app.db.database import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(accounts.router)