#!/bin/bash
set -e  # Exit immediately if any command fails

echo "Step 1: Building Docker image..."
docker compose build

echo "Step 2: Starting containers..."
docker compose up -d

echo "App has been deployed and running on http://localhost:8000/docs"
