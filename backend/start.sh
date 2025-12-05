#!/bin/bash
# Start script for Render deployment

# Create necessary directories
mkdir -p reports
mkdir -p logs
mkdir -p uploads

# Start the application
uvicorn app.main:app --host 0.0.0.0 --port ${PORT:-8000}

