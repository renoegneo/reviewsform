from fastapi import FastAPI
from app.routers import reviews
from app.db import engine, Base

app = FastAPI(title="Reviews API")

# create tables (for demo). In production use alembic migrations.
Base.metadata.create_all(bind=engine)

app.include_router(reviews.router)