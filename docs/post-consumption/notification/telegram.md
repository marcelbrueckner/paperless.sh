---
title: Telegram
---

# Telegram notification

This script allows to receive notifications about consumed documents via Telegram Messenger.

## Prerequisites

1. A Telegram bot created via [@botfather](https://t.me/botfather).
2. The following additional Python package installed on your system:
    * python-telegram-bot

    !!! note
        If you're running Paperless-ngx via Docker, you will need to add a [custom container initialization script](../../other/custom-cont-init.md) for this.

## Script

=== ".env"

    ```bash
    # Token to access the HTTP API
    TELEGRAM_BOT_TOKEN=

    # https://api.telegram.org/bot<TELEGRAM_BOT_TOKEN>/getUpdates
    TELEGRAM_CHAT_ID=
    ```

=== "pngx-notify-telegram.py"

    ```python
    --8<-- "scripts/post-consumption/notification/telegram/pngx-notify-telegram.py"
    ```

=== "post-consumption-wrapper.sh"

    ```bash
    # Notify about new document via Telegram
    python ${SCRIPT_DIR}/pngx-notify-telegram.py
    ```

=== "10-install-additional-packages.sh"

    ```python
    --8<-- "scripts/post-consumption/notification/telegram/10-install-additional-packages.sh"
    ```

## Notes

Script files can also be found on [GitHub](https://github.com/marcelbrueckner/paperless.sh/tree/main/scripts/post-consumption/notification/telegram).
