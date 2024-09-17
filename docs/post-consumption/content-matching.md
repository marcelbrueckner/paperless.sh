---
title: Content matching
---

# Document content matching

Paperless-ngx does a great job matching documents with correct correspondents, storage path etc.
However, there are documents for which the automatic matching doesn't work or a single regular expression match isn't sufficient.
For such cases, further examining the document's content after consumption is necessary.

## Update document details via organize and the Paperless-ngx CLI

[organize](https://github.com/tfeldmann/organize) is an open-source, command-line file management automation tool.
It allows to execute certain actions based on custom filters. These can be easily defined in YAML.

Probably the most helpful filter in this context is the `filecontent` filter. The document's content can be matched with regular expressions which allows to dynamically re-use (parts of) the matched content in subsequent actions.

Following script

1. ensures that a newly-consumed document gets assigned a proper title based on the document's content.
    This helps to stick to a consistent naming pattern for documents that you receive regularly, e.g. invoices.
2. extracts a value out of the document content and stores it in a given custom field

The Paperless-ngx CLI can be used to update other fields as well. Check the CLI's help or [GitHub repository](https://github.com/marcelbrueckner/paperless-ngx-cli) for more information.

### Prerequisites

For this solution to work, you will need to install the following packages:

* [organize-tool](https://pypi.org/project/organize-tool/)
* [poppler](https://poppler.freedesktop.org/)[^1]
* [pypaperless-cli](https://pypi.org/project/pypaperless-cli/)

[^1]: Poppler is required for organize's `filecontent` filter to work, see [https://github.com/tfeldmann/organize/issues/322](https://github.com/tfeldmann/organize/issues/322).

As organize will leverage the API for updating the document title, the [API prerequisites](../api/README.md) apply as well.

### Structure

Sticking to the general idea of our scripts folder layout, we will end up with following structure for this solution.

```bash
paperless-ngx/
├─ my-post-consumption-scripts/
│  ├─ organize/
│  │  └─ organize.config.yml.tpl
│  └─ post-consumption-wrapper.sh
│  # Obviously the below file only exists
│  # if you're running Paperless-ngx via Docker Compose
├─ my-custom-container-init/
│  └─ 10-install-additional-packages.sh
└─ docker-compose.yml
```

### Scripts

=== ".env"

    ```bash
    # Token to access the REST API
    PNGX_TOKEN=
    # Your Paperless-ngx URL, without trailing slash
    # If running your post-consumption script within Docker, its likely to be http://localhost:8000
    PNGX_HOST=
    ```

=== "organize.config.yml.tpl"

    ```yaml
    --8<-- "scripts/post-consumption/content-matching/organize.config.yml.tpl"
    ```

=== "post-consumption-wrapper.sh"

    ```bash
    --8<-- "scripts/post-consumption/content-matching/post-consumption-wrapper.sh"
    ```

=== "10-install-additional-packages.sh"

    ```bash
    --8<-- "scripts/post-consumption/content-matching/10-install-additional-packages.sh"
    ```

## Notes

Script files can also be found on [GitHub](https://github.com/marcelbrueckner/paperless.sh/tree/main/scripts/post-consumption/content-matching).
