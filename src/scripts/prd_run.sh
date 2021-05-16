#!/bin/bash
set -e
set -x

# run dev
read_var() {
    VAR=$(grep $1 $2 | xargs)
    IFS="=" read -ra VAR <<< "$VAR"
    echo ${VAR[1],,}
}

LOGURU_LOGGING_LEVEL=$(read_var LOGURU_LOGGING_LEVEL .env)
WORKERS=$(read_var WORKERS .env)
gunicorn -c gunicorn_cfg.py main:app
#--log-level ${LOGURU_LOGGING_LEVEL,,}
# uvicorn main:app --port 5000 --workers $((WORKERS)) --log-level  ${LOGURU_LOGGING_LEVEL,,}