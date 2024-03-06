#!/usr/bin/env python

# Work in progress
# Only allows updating the title and a single custom field at the moment

import argparse, httpx, os, sys

parser = argparse.ArgumentParser(description='Update a single document via Paperless-ngx REST API')
parser.add_argument('--url',
    dest='url',
    action='store',
    help='Your Paperless-ngx URL',
    default=os.environ.get('PAPERLESS_URL')
)
parser.add_argument('--auth-token',
    dest='token',
    action='store',
    help='Your Paperless-ngx REST API authentication token',
    default=os.environ.get('PAPERLESS_TOKEN')
)
parser.add_argument('--document-id',
    dest='id',
    type=int,
    action='store',
    help='ID of the document that should be updated',
    required=True
)
parser.add_argument('--title',
    dest='title',
    action='store',
    help='Set the document title'
)
parser.add_argument('--custom-field-id',
    dest='custom_field_id',
    type=int,
    action='store',
    help='ID of the custom field that should be updated'
)
parser.add_argument('--custom-field-value',
    dest='custom_field_value',
    action='store',
    help='Value of the custom field that should be stored'
)
args = parser.parse_args()

headers = {'Authorization': f'Token {args.token}'}
data = {}

# Update title
if args.title is not None:
    data['title'] = args.title

# Update custom field
# Only if both --custom-field-id and --custom-field-value have been specified
if all(param is not None for param in [args.custom_field_id, args.custom_field_value]):
    new_field = {
        "field": args.custom_field_id,
        "value": args.custom_field_value
    }

    # Even when patching a single custom field, we need to include all of the document's existing custom fields
    # Otherwise, other custom fields will be removed from the document
    response = httpx.get(f"{args.url}/api/documents/{args.id}/", headers=headers)

    if response.is_error:
        msg = "HTTP error {} while trying to obtain document details via REST API at {}."
        sys.exit(msg.format(response.status_code, args.url))
    
    data['custom_fields'] = response.json()['custom_fields']

    # Update custom field value "in-place" if already attached to document (to keep custom field order)
    if any(custom_field['field'] == args.custom_field_id for custom_field in data['custom_fields']):
        data['custom_fields'] = [(new_field if custom_field['field'] == args.custom_field_id else custom_field) for custom_field in data['custom_fields']]
    # Otherwise, simply append to the list
    else:
        data['custom_fields'] = data['custom_fields'].append(new_field)

if data:
    response = httpx.patch(f"{args.url}/api/documents/{args.id}/", headers=headers, json=data)

    if response.is_error:
        msg = "HTTP error {} while trying to update document via REST API at {}."
        sys.exit(msg.format(response.status_code, args.url, data))

    print(f"Document with ID {args.id} successfully updated")
