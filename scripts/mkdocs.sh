#!/bin/bash
set -e
set -x

# mkdocs
mkdocs build

# Copy Contribute to Github Contributing
cp ~/test-api/docs/index.md ~/test-api/README.md
cp ~/test-api/docs/contribute.md ~/test-api/CONTRIBUTING.md

mkdocs gh-deploy
