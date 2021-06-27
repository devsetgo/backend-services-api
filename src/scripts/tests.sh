#!/bin/bash
set -e
set -x

# clear log file if it exists
if [[ -f "~/backend-services-api/logging/log.log" ]]
then
    echo "Removing ~/backend-services-api/logging/log.log"
    rm ~/backend-services-api/logging/log.log
fi

echo "log cleared"
#run pre-commit
pre-commit run -a
# Change to test environment
sed -i 's/RELEASE_ENV=.*/RELEASE_ENV="test"/' .env

python3 -m pytest
# python3 -m pytest -v -s
sed -i "s/<source>\/home\/mike\/backend-services-api\/src<\/source>/<source>\/github\/workspace\/src<\/source>/g" /home/mike/backend-services-api/src/coverage.xml
# create coverage-badge
coverage-badge -o ../coverage.svg -f


# remove test.db if it exists
if [[ -f "~/backend-services-api/sqlite_db/test.db" ]]
then
    echo "Removing ~/backend-services-api/sqlite_db/test.db"
    rm ~/backend-services-api/sqlite_db/test.db
fi

echo "db removed"
# generate flake8 report
flake8 --tee . > flake8_report/report.txt
# Reset to original release env
sed -i 's/RELEASE_ENV=.*/RELEASE_ENV="prd"/' .env
