#!/bin/bash
set -e
set -x

# rm logfile/app_log.log
echo "log cleared"

# delete db
# rm sqlite_db/api.db
echo "db removed"
# run isort recursively
# isort -rc .

#run pre-commit
pre-commit run -a

# bash scripts/test.sh --cov-report=html ${@}
python3 -m pytest
# python3 -m pytest -v -s
sed -i "s/<source>\/home\/mike\/test-api\/src<\/source>/<source>\/github\/workspace\/src<\/source>/g" /home/mike/test-api/src/coverage.xml
# create coverage-badge
coverage-badge -o ../coverage.svg -f
# delete db
# rm sqlite_db/api.db
# echo "db removed"
# generate flake8 report
flake8 --tee . > flake8_report/report.txt
