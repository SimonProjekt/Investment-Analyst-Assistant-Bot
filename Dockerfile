FROM python:3.11-slim

RUN apt-get update && apt-get install -y \
    gcc \
    libsqlite3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY . .

ENV PYTHONPATH=/app

RUN pip install --no-cache-dir -r requirements.txt

# Starta med att bygga databasen och sen starta servern
CMD ["bash", "-c", "python services/database_service.py && uvicorn main:app --host 0.0.0.0 --port 8000"]
