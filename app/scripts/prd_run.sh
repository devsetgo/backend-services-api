#!/bin/bash
set -e
set -x

# run dev
# uvicorn main:app --port 5000 --workers 2
gunicorn -c gunicorn_cfg.py main:app
