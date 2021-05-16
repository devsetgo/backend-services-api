#!/bin/bash
set -e
set -x

# run dev
# read_var() {
#     VAR=$(grep $1 $2 | xargs)
#     IFS="=" read -ra VAR <<< "$VAR"
#     echo ${VAR[1],,}
# }

# LOGURU_LOGGING_LEVEL=$(read_var LOGURU_LOGGING_LEVEL .env)
# WORKERS=$(read_var WORKERS .env)
# gunicorn -c gunicorn_cfg.py main:app --spew
#--log-level ${LOGURU_LOGGING_LEVEL,,}
# uvicorn main:app --port 5000 --workers $((WRKRS)) --log-level  ${LOGURU_LOGGING_LEVEL,,}
echo "starting container for ${TITLE}"
gunicorn main:app --workers $((WRKRS)) --bind 0.0.0.0:5000 --worker-class uvicorn.workers.UvicornH11Worker --log-level ${LOGURU_LOGGING_LEVEL,,}