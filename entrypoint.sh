#!/bin/sh

gunicorn src.main:app --bind $FASTAPI_HOST:$FASTAPI_PORT --workers $WORKERS --worker-class uvicorn.workers.UvicornWorker