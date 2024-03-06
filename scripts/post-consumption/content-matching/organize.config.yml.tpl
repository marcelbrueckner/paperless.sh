# organize configuration file
# https://organize.readthedocs.io

# YAML ANCHORS
# This filters the exact document that has been consumed
.locations: &current_document
  - path: "{env.DOCUMENT_ARCHIVE_DIR}"
    filter:
      # Needs to be replaced with e.g. `envsubst`
      # as organize doesn't replace environment placeholders in filter
      - "$DOCUMENT_ARCHIVE_FILENAME"

# RULES
rules:
  - name: "Nabu Casa invoice"
    locations: *current_document
    filters:
      - filecontent: "Nabu Casa"
      - filecontent: "(?P<title>Home Assistant Cloud)"
      - filecontent: 'Amount due.*(?P<amount>\d{2}\.\d{2})'
    actions:
      - echo: "Home Assistant hooray"
      - shell: "./pngx-update-document.py --url http://localhost:8000 --document-id {env.DOCUMENT_ID} --title '{filecontent.title}' --custom-field-id 1 --custom-field-value {filecontent.amount}"
      - echo: "{shell.output}"
