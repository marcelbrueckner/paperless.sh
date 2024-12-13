"""
examples for
MYTOKEN="3fe723423dsd459266cec5e9ce81420c4fc2771",
MYURL "http://paperless:8000" 
SEARCHPATH="?tags__id__all=2&custom_field_query=%5B%22OR%22,%5B%5B2,%22exists%22,%22false%22%5D%5D%5D&query=created:%5B-3%20month%20to%20now%5D,added:%5B-1%20week%20to%20now%5D&sort=added&reverse=1&page=1",
"""
settings = dict(
    MYTOKEN="3fe723423dsd459266cec5e9ce81420c4fc2771",
    MYURL="http://paperless.example.com:8000",
    SEARCHPATH="?tags__id__all=2&custom_field_query=%5B%22OR%22,%5B%5B2,%22exists%22,%22false%22%5D%5D%5D&query=created:%5B-3%20month%20to%20now%5D,added:%5B-1%20week%20to%20now%5D&sort=added&reverse=1&page=1",
    TO=["joe.sixpack@example.com"],
    FROM="joe.sixpack@example.com+paperless@gmail.com",
    SUBJECT="Paperless files in need of attendance.",
    SMTP_HOST="localhost",
    SMTP_PORT=25,
    SMTP_USER="USER",
    SMTP_PASS=""
)