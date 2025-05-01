#!/usr/bin/env bash
set -e

echo "🧱 Installerar beroenden..."
pip install -r requirements.txt

echo "🧠 Bygger RAG-databas från .md-filer..."
PYTHONPATH=$(pwd) python services/database_service.py

echo "✅ Build klart"
