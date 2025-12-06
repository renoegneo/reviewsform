from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import reviews
from app.db import engine, Base

app = FastAPI(title="Reviews API")

# CORS - разрешаем запросы с Vercel
app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://reviewsform.vercel.app",
        "https://reviewsform-git-main-renoegneos-projects-63bc2665.vercel.app",
        "https://reviewsform-e4uh9wzm0-renoegneos-projects-63bc2665.vercel.app",
        "https://*.vercel.app",
        "http://localhost:8080",
        "http://127.0.0.1:8080"
    ],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# Создание таблиц (для первого запуска)
Base.metadata.create_all(bind=engine)

# Подключение роутеров
app.include_router(reviews.router)