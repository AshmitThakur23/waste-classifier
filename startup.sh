#!/bin/bash
cd backend
gunicorn --bind=0.0.0.0:8000 --timeout 600 --workers 1 app:app -k uvicorn.workers.UvicornWorker
