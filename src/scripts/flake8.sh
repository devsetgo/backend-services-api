#!/bin/bash
set -e
set -x

# generate flake8 report
flake8 --tee . > flake8_report/report.txt
