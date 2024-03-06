---
title: Container init
---

# Custom container initialization

Some scripts of this collection depend on additional packages or command-line tools that aren't shipped with the Paperless-ngx container image by default.
Instead of building your own Docker image, Paperless-ngx allows you to customize your container on startup by using [custom container initialization](https://docs.paperless-ngx.com/advanced_usage/#custom-container-initialization) scripts.

## Setup

Create a folder `my-custom-init-scripts/` next to your `docker-compose.yml` and create one or more initialization scripts.
The initialization scripts itself simply contain the command you would otherwise execute in your Terminal to install the desired package(s)
and will be executed in lexical order. See the examples below for details.

```bash
paperless-ngx/
├─ my-custom-init-scripts/
│  │  # Will be executed in lexical order
│  ├─ 10-base-init-script.sh
│  └─ 20-something-different.sh
└─ docker-compose.yml
```

Make sure `my-custom-init-scripts/` and the files herein are executable and owned by `root`. Otherwise they won't be executed.

```bash
chown -R root:root my-custom-init-scripts/
chmod -R 0755 my-custom-init-scripts/
```

In your `docker-compose.yml` add the following to your webserver service and re-create your container:

```yaml title="docker-compose.yml"
services:
  # ...
  webserver:
    # ...
    volumes:
      - ./my-custom-init-scripts:/custom-cont-init.d:ro 
```

Upon the next start of your container, the script will be executed and packages will be installed.

## Examples

### Install additional Python packages

Create an initialization script[^1] with the following content:

```bash
#!/usr/bin/env bash
pip install --root-user-action=ignore python-telegram-bot
```

[^1]: The actual filename doesn't matter.