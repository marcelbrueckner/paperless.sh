#!/usr/bin/env python

import os
import asyncio
from pypaperless import Paperless

PAPERLESS_URL = os.environ["PAPERLESS_URL"]
PAPERLESS_TOKEN = os.environ["PAPERLESS_TOKEN"]

# Custom field IDs to sum up
CUSTOM_FIELD_ID = 1

# Visit https://your-paperless-url/api/documents in your browser
# to discover all available filters
filters = {
    "tags__id": 38,
    "document_type__id": 3,
    "created__date__gt": "2023-10-01",
    "created__date__lt": "2023-12-31"
}

async def main():
    paperless = Paperless(PAPERLESS_URL, PAPERLESS_TOKEN)

    async with paperless:
        async with paperless.documents.reduce(**filters) as filtered:
            sum = 0
            async for doc in filtered:
                sum += [f.value for f in doc.custom_fields if f.field == CUSTOM_FIELD_ID][0]

    print(sum)

asyncio.run(main())
