FROM python:3.14-slim

WORKDIR /app

# Копируем backend в контейнер
COPY backend/ /app
COPY .env /app/.env


RUN pip install --no-cache-dir -r requirements.txt

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
