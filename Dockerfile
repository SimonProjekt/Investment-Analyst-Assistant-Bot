# Starta från en slimmad Python-bild
FROM python:3.11-slim

# Installera systemberoenden (Chroma kräver gcc, sqlite m.m.)
RUN apt-get update && apt-get install -y \
    gcc \
    libsqlite3-dev \
    git \
    && rm -rf /var/lib/apt/lists/*

# Ange arbetsmapp i containern
WORKDIR /app

# Kopiera projektet
COPY . .

# Installera Python-beroenden
RUN pip install --no-cache-dir -r requirements.txt

# Skapa databasen automatiskt
RUN python services/database_service.py

# Starta FastAPI
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
