#!/usr/bin/env bash

# paperless-ngx post-consumption script
#
# https://docs.paperless-ngx.com/advanced_usage/#post-consume-script
#

SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

# Add additional information to document
# Make sure organize-tool and poppler-utils has been installed
# on your system (resp. container, via custom-cont-init.d)

# organize-tool doesn't accept full file path as argument
# but expects directory and filename pattern without extension instead
export DOCUMENT_ARCHIVE_FILENAME=$(basename "${DOCUMENT_ARCHIVE_PATH}")
export DOCUMENT_ARCHIVE_DIR=$(dirname "${DOCUMENT_ARCHIVE_PATH}")

# While organize supports environment variables as placeholders in it's configuration,
# it's not yet supported everywhere in the configuration (e.g. filters),
# thus leveraging envsubst to replace environment placeholders
ORGANIZE_CONFIG_PATH=$(mktemp --suffix=.yml ${TMPDIR:-/tmp}/organize.config.XXXXXX)
envsubst < "${SCRIPT_DIR}/organize/organize.config.yml.tpl" > "${ORGANIZE_CONFIG_PATH}"

# Execute configured actions
# Add `--format errorsonly` to suppress most of organize's output in logs
organize run "${ORGANIZE_CONFIG_PATH}" --working-dir "${SCRIPT_DIR}/organize"

# Clean up
rm -f "${ORGANIZE_CONFIG_PATH}"
