#!/bin/bash
set -e
set -x

# Create a UML image
# Requires Graphviz installed (sudo apt-get install graphviz) on the host

pyreverse -o png src/

mv ~/backend-services-api/classes.png ~/backend-services-api/docs/images/