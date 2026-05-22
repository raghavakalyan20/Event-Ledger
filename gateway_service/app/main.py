from fastapi import FastAPI
from app.api import events, health
from app.db.database import engine
from app.db.models import Base

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Gateway Service")

app.include_router(events.router)
app.include_router(health.router)