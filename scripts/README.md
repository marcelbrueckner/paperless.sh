# Paperless scripts collection

This folder contains the actual scripts that are referenced on [paperless.sh](https://paperless.sh), except short snippets that might have been provided inline.

## Structure

For easy reference, the script path should match the path of the corresponding description in [`docs/`](../docs/).
If a solution documentation consists of multiple scripts, corresponding scripts should be placed within an identically-named folder.

A solution documentation for sending notifications via Telegram documented here ...

```bash
docs/post-consumption/notification/telegram.md
```

... should resemble to a script path given below.

```bash
# Folder-based for either single or multiple scripts
scripts/post-consumption/notification/telegram/<SCRIPTS_HERE>

# Optionally an identically named script instead of folder if single script
scripts/post-consumption/notification/telegram.py
```
