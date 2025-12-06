from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware  # добавь импорт
from app.routers import reviews
from app.db import engine, Base

app = FastAPI(title="Reviews API")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # В проде замени на конкретный домен
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

Base.metadata.create_all(bind=engine)
app.include_router(reviews.router)

