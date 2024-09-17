#!/usr/bin/env bash

# Install additional packages

# Add additional information to consumed documents
# based on hypercomplex ;) rules
# https://github.com/tfeldmann/organize/
# https://github.com/marcelbrueckner/paperless-ngx-cli
apt-get install poppler-utils
pip install --root-user-action=ignore organize-tool
pip install --root-user-action=ignore pypaperless-cli
