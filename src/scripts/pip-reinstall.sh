#!/bin/bash
set -e
set -x

# remove dev dependencies
pip3 uninstall -r requirements/dev.txt -y
# upgrade pip
pip3 install --upgrade pip setuptools
# install dev dependencies
pip3 install -r requirements/dev.txt
