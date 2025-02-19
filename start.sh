#!/bin/bash

# Set default port if not provided
PORT=${PORT:-8000}

# Ensure we're in the correct directory
cd "$(dirname "$0")/backend" || exit 1

# Start the application with proper error handling
python -m uvicorn app.main:app --host 0.0.0.0 --port ${PORT} --no-access-log
