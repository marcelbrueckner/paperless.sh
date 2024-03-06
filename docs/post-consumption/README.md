---
title: Overview
---

# Post-consumption scripts

> Executed after the consumer has successfully processed a document and has moved it into paperless.
&mdash; [Paperless-ngx documentation](https://docs.paperless-ngx.com/advanced_usage/#post-consume-script)

## Setup

Paperless-ngx supports a single post-consumption script. However, it's perfectly fine to call other scripts from it.
This way, you can nicely separate post-consumption scripts for different tasks. Those scripts can also be written in different languages.

Assuming a folder `my-post-consumption-scripts/`[^1] with the following structure.
[^1]: That's just an example. It's not strictly necessary to separate pre- and post-consumption scripts. In fact, scripts can be stored everywhere on your system as long as Paperless-ngx is able to access it. But it may help to store your scripts alongside each other.

```bash
paperless-ngx/
├─ my-post-consumption-scripts/
│  │  # Sort your scripts into subfolders if you like
│  ├─ custom-script-01/
│  │  └─ actual-post-consumption-task-01.sh
│  ├─ custom-script-02/
│  │  └─ actual-post-consumption-task-02.py
│  └─ post-consumption-wrapper.sh
│  # Obviously the below file only exists
│  # if you're running Paperless-ngx via Docker Compose
└─ docker-compose.yml
```

The post-consumption "wrapper" just contains some helper variables and calls to your actual post-consumption scripts.

```bash title="post-consumption-wrapper.sh"
#!/usr/bin/env bash

# paperless-ngx post-consumption script
#
# https://docs.paperless-ngx.com/advanced_usage/#post-consume-script
#

SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

# Have something written into Paperless-ngx logs
echo "Hello. Post-consumption script here."

bash ${SCRIPT_DIR}/custom-script-01/actual-post-consumption-task-01.sh
python ${SCRIPT_DIR}/custom-script-02/actual-post-consumption-task-02.py
```

## Examples

Have a look at the examples via the navigation on the left side.
