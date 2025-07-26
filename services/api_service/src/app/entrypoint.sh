#!/bin/bash
set -e

# Enter the application directory
ls -la

echo "🔁 Running Alembic migrations..."
alembic upgrade head  # No need to specify `-c app/alembic.ini` if already inside /src/app

echo "🚀 Starting FastAPI server..."
exec python -m uvicorn main:app --host 0.0.0.0 --port 8000
