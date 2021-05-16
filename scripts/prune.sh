#!/bin/bash
set -e
set -x

# Container prune
docker container prune

# install requirements
docker image prune --all