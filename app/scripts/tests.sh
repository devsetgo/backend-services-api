#!/bin/bash
set -e
set -x

# run isort recursively
# isort -rc .

#run pre-commit
pre-commit run -a

# bash scripts/test.sh --cov-report=html ${@}
python3 -m pytest
# python3 -m pytest -v -s

# create coverage-badge
coverage-badge -o ../coverage.svg -f

# generate flake8 report
flake8 --tee . > flake8_report/report.txt

# delete db
rm sqlite_db/api.db
echo "db removed"


