#!/bin/bash
set -e
set -x

#delete db
if [[ -f ~/test-api/src/sqlite_db/api.db ]]
then
    echo "deleting db"
    rm ~/test-api/src/sqlite_db/api.db
fi

#delete logs
if [[ -f ~/test-api/src/log/log.log ]]
then
    echo "deleting log"
    rm ~/test-api/src/log/log.log
fi

# run dev
read_var() {
    VAR=$(grep $1 $2 | xargs)
    IFS="=" read -ra VAR <<< "$VAR"
    echo ${VAR[1],,}
}

LOGURU_LOGGING_LEVEL=$(read_var LOGURU_LOGGING_LEVEL .env)

uvicorn main:app --port 5000 --reload --log-level ${LOGURU_LOGGING_LEVEL,,}