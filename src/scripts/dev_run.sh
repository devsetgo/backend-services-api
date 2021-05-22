#!/bin/bash
set -e
set -x

read_var() {
    VAR=$(grep $1 $2 | xargs)
    IFS="=" read -ra VAR <<< "$VAR"
    echo ${VAR[1],,}
}

LOGURU_LOGGING_LEVEL=$(read_var LOGURU_LOGGING_LEVEL .env)
# run dev
uvicorn main:app --port 5000 --reload --log-level ${LOGURU_LOGGING_LEVEL,,}