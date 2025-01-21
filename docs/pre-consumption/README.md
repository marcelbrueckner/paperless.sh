---
title: Overview
---

# Pre-consumption scripts

> Executed after the consumer sees a new document in the consumption folder, but before any processing of the document is performed.
&mdash; [Paperless-ngx documentation](https://docs.paperless-ngx.com/advanced_usage/#pre-consume-script)

## Setup

Paperless-ngx supports a single pre-consumption script. However, it's perfectly fine to call other scripts from it.
This way, you can nicely separate pre-consumption scripts for different tasks. Those scripts can also be written in different languages.

Assuming a folder `my-pre-consumption-scripts/`[^1] with the following structure.
[^1]: That's just an example. It's not strictly necessary to separate pre- and post-consumption scripts. In fact, scripts can be stored everywhere on your system as long as Paperless-ngx is able to access it. But it may help to store your scripts alongside each other.

```bash
paperless-ngx/
├─ my-pre-consumption-scripts/
│  │  # Sort your scripts into subfolders if you like
│  ├─ custom-script-01/
│  │  └─ actual-pre-consumption-task-01.sh
│  ├─ custom-script-02/
│  │  └─ actual-pre-consumption-task-02.py
│  └─ pre-consumption-wrapper.sh
│  # Obviously the below file only exists
│  # if you're running Paperless-ngx via Docker Compose
└─ docker-compose.yml
```

The pre-consumption "wrapper" just contains some helper variables and calls to your actual pre-consumption scripts.

<a name="pre-consumption-wrapper"></a>

```bash title="pre-consumption-wrapper.sh"
#!/usr/bin/env bash

# paperless-ngx pre-consumption script
#
# https://docs.paperless-ngx.com/advanced_usage/#pre-consume-script
#

SCRIPT_PATH=$(readlink -f "$0")
SCRIPT_DIR=$(dirname "$SCRIPT_PATH")

# Have something written into Paperless-ngx logs
echo "Hello. Pre-consumption script here."

bash ${SCRIPT_DIR}/custom-script-01/actual-pre-consumption-task-01.sh
python ${SCRIPT_DIR}/custom-script-02/actual-pre-consumption-task-02.py
```

## Examples

Have a look at the examples via the navigation on the left side.
