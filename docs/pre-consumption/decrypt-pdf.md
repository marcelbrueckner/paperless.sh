# Decrypt PDFs before consumption

Encrypted PDFs are one way to rain on your parade with paperless-ngx - even if you know the password. You get no thumbnail, no OCR, you are constantly nagged for the password when you want to view the file. So let's get rid of the encryption!

## Setup
_decrypt-pdf_ consists of
1. the script itself
2. the password files (insecure.pwd.txt and personal.pwd.txt)
   * **personal.pwd.txt** is slated for your personal passwords, it's also added to the local _.gitignore_ file
   * **insecure.pwd.txt** contains some of the most prolific passwords I could find
   * you can create other files in the same manner to try passwords from dumps, "most common password in XXX" lists etc.

Keep all of these in the same folder and install the script either as your one pre-consumption script or call it via other means, e.g. the [example pre-consumption consolidated wrapper script](./README.md#pre-consumption-wrapper).

