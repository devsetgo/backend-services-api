#!/bin/bash
set -e
set -x

rm ~/backend-services-api/logging/log.log
echo "log cleared"
#run pre-commit
pre-commit run -a
# Change to test environment
sed -i 's/RELEASE_ENV=.*/RELEASE_ENV="test"/' .env

python3 -m pytest
# python3 -m pytest -v -s
sed -i "s/<source>\/home\/mike\/backend-services-api\/src<\/source>/<source>\/github\/workspace\/backend-services-api\/src<\/source>/g" /home/mike/backend-services-api/src/coverage.xml
# create coverage-badge
coverage-badge -o ../coverage.svg -f
# delete db
rm ~/backend-services-api/sqlite_db/test.db
echo "db removed"
# generate flake8 report
flake8 --tee . > flake8_report/report.txt
# Reset to original release env
sed -i 's/RELEASE_ENV=.*/RELEASE_ENV="prd"/' .env