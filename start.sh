#!/bin/bash
cd /app
python -m uvicorn backend.app.main:app --host 0.0.0.0 --port $PORT --no-access-log
