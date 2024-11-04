---
title: Decrypt PDF
---

# Decrypt PDFs before consumption

Encrypted PDFs are one way to rain on your parade with paperless-ngx - even if you know the password. You get no thumbnail, no OCR, you are constantly nagged for the password when you want to view the file. So let's get rid of the encryption!

## Setup
_decrypt-pdf_ consists of
1. the script itself
2. **passwords.txt** containinig all passwords you want to try out on your consumed pdfs

Keep these files in the same folder as the script and install the script either as your one pre-consumption script or call it via other means, e.g. the [example pre-consumption consolidated wrapper script](./README.md#pre-consumption-wrapper).

