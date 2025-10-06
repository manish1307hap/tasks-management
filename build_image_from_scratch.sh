#!/bin/bash
set -e  # Exit immediately if any command fails

echo "Step 1: Building Docker image..."
docker compose build

echo "Step 2: Running Alembic migrations..."
docker compose run --rm web alembic upgrade head

echo "Step 3: Starting containers..."
docker compose up -d

echo "FastAPI should be running on http://localhost:8000/docs"
