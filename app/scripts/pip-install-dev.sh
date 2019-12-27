#!/bin/bash
set -e
set -x

# upgrade pip
pip3 install --upgrade pip setuptools
# install dev dependencies
pip3 install -r requirements/dev.txt
