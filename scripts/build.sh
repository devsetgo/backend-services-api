#!/bin/bash
set -e
set -x

# upgrade
# docker build -t mikeryan56/test-api -f dockerfile_pypy .

CAL_VER=$(date '+%Y-%m-%d')
echo 'Docker Build Python'
docker build -t mikeryan56/test-api:$CAL_VER-python38 -t mikeryan56/test-api:latest -f ./dockerfiles/dockerfile_python .
# echo "Running Docker Image"
# docker run mikeryan56/test-api:$CAL_VER-python38
echo "Push"
docker push mikeryan56/test-api:$CAL_VER-python38
docker push mikeryan56/test-api:latest
# echo 'Docker Build with PyPy'
# docker build -t mikeryan56/test-api:$CAL_VER -f ./docker/dockerfile_pypy .

