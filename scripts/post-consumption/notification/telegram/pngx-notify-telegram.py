#!/usr/bin/env python

import os
import asyncio
import telegram
import re
from datetime import datetime, timedelta
from textwrap import dedent

TOKEN = os.getenv('TELEGRAM_BOT_TOKEN')
CHAT_ID = os.environ.get('TELEGRAM_CHAT_ID')
PAPERLESS_URL = os.environ.get('PAPERLESS_URL')

# Document information
# Can be used to compose a custom notification message (see further below)
DOCUMENT_ID = os.environ.get('DOCUMENT_ID')
DOCUMENT_FILE_NAME = os.environ.get('DOCUMENT_FILE_NAME')
DOCUMENT_ARCHIVE_PATH = os.environ.get('DOCUMENT_ARCHIVE_PATH')
DOCUMENT_SOURCE_PATH = os.environ.get('DOCUMENT_SOURCE_PATH')
DOCUMENT_CREATED = os.environ.get('DOCUMENT_CREATED')
DOCUMENT_ADDED = os.environ.get('DOCUMENT_ADDED')
DOCUMENT_MODIFIED = os.environ.get('DOCUMENT_MODIFIED')
DOCUMENT_THUMBNAIL_PATH = os.environ.get('DOCUMENT_THUMBNAIL_PATH')
DOCUMENT_DOWNLOAD_URL = os.environ.get('DOCUMENT_DOWNLOAD_URL')
DOCUMENT_THUMBNAIL_URL = os.environ.get('DOCUMENT_THUMBNAIL_URL')
DOCUMENT_CORRESPONDENT = os.environ.get('DOCUMENT_CORRESPONDENT')
DOCUMENT_TAGS = os.environ.get('DOCUMENT_TAGS')
DOCUMENT_ORIGINAL_FILENAME = os.environ.get('DOCUMENT_ORIGINAL_FILENAME')
TASK_ID = os.environ.get('TASK_ID')

async def send_message():
    # Adjust according to your timezone, e.g. Europe/Berlin is UTC+1
    document_date = datetime.fromisoformat(DOCUMENT_CREATED) + timedelta(hours=1)
    message = f"""
        A new document has been added.

        ID: {DOCUMENT_ID}
        Correspondent: {DOCUMENT_CORRESPONDENT}
        Filename: {DOCUMENT_ORIGINAL_FILENAME}
        Date created: {document_date.date()}

        Preview: {PAPERLESS_URL}/api/documents/{DOCUMENT_ID}/preview/
        Details: {PAPERLESS_URL}/documents/{DOCUMENT_ID}/details

        Tags:
        {DOCUMENT_TAGS}
    """

    message = re.sub(r'[_*[\]()~`>#\+\-=|{}.!]', r'\\\g<0>', message)
    message = dedent(message)

    bot = telegram.Bot(token=TOKEN)
    await bot.send_photo(
        chat_id     =   CHAT_ID,
        photo       =   open(DOCUMENT_THUMBNAIL_PATH, 'rb'),
        caption     =   message,
        parse_mode  =   telegram.constants.ParseMode.MARKDOWN_V2
    )

def main() -> None:
    asyncio.run(send_message())

if __name__ == "__main__":
    main()
