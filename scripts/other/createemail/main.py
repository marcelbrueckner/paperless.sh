"""
Author: Your Name
Date: 2024-12-12
Synopsis: This script retrieves documents, correspondents, and tags from a Paperless instance, 
          formats their information into an HTML email, and sends it via a local Postfix server.

License (MIT): See the previous example.
"""

import requests
import smtplib
from config import settings
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from datetime import datetime, date

TOKEN = settings["MYTOKEN"]
MYURL = settings["MYURL"]  # e.g. "http://paperless:8000" (no /api here)
SEARCHPATH = settings["SEARCHPATH"]  # Configurable search path for documents
TO = settings["TO"]   # Can be a string or a list
FROM = settings["FROM"]
SUBJECT = settings["SUBJECT"]

headers = {
    "Authorization": f"Token {TOKEN}",
    "Accept": "application/json"
}

def safe_request(url):
    """Make a request and handle exceptions."""
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data from {url}: {e}")
        return None

def get_correspondents():
    url = f"{MYURL}/api/correspondents/"
    data = safe_request(url)
    if not data:
        return []
    return [
        {"id": c["id"], "correspondent": c["name"]}
        for c in data.get("results", [])
        if "id" in c and "name" in c
    ]

def get_tags_map():
    url = f"{MYURL}/api/tags/"
    data = safe_request(url)
    if not data:
        return {}
    return {t["id"]: t["name"] for t in data.get("results", []) if "id" in t and "name" in t}

def get_documents():
    """Fetch documents using the configurable SEARCHPATH."""
    url = f"{MYURL}/api/documents/{SEARCHPATH}"
    data = safe_request(url)
    if not data:
        return []
    return data.get("results", [])

def get_document_details(doc_id):
    url = f"{MYURL}/api/documents/{doc_id}/"
    data = safe_request(url)
    if not data:
        return "N/A", "N/A", None
    return (
        data.get("original_file_name", "N/A"),
        data.get("archived_file_name", "N/A"),
        data.get("created_date", None),
    )

def calculate_age(created_date_str):
    if not created_date_str:
        return "N/A"
    try:
        created_date = datetime.strptime(created_date_str, "%Y-%m-%d").date()
        today = date.today()
        age_days = (today - created_date).days
        return age_days
    except ValueError:
        return "N/A"

def create_email(docs, correspondents, tag_map):
    corr_map = {c["id"]: c["correspondent"] for c in correspondents}

    # Sort documents by Age (descending)
    sorted_docs = sorted(
        docs,
        key=lambda d: calculate_age(d.get("created_date")),
        reverse=True,
    )

    lines = []
    for doc in sorted_docs:
        try:
            doc_id = doc.get("id")
            corr_id = doc.get("correspondent")
            doc_tags = doc.get("tags", [])

            if not doc_id:
                continue

            corr_name = corr_map.get(corr_id, "No Correspondent")

            original_file_name, archived_file_name, created_date_str = get_document_details(doc_id)
            age = calculate_age(created_date_str)

            # Format age
            if isinstance(age, int) and age > 31:
                age_str = f"<span style='color:red;'>{age}</span>"
            else:
                age_str = str(age)

            # Map tag IDs to names
            tag_names = [tag_map.get(tid, f"Tag-{tid}") for tid in doc_tags]
            tags_str = ", ".join(tag_names) if tag_names else "None"

            # Make the correspondent's name the link to the file
            detail_url = f"{MYURL}/documents/{doc_id}/"
            corr_link = f"<a href='{detail_url}'><b>{corr_name}</b></a>"

            # Add blank line before each bullet
            lines.append(
                f"<br><li>"
                f"{corr_link}<br>"
                f"<b>Age (days)</b>: {age_str}<br>"
                f"<b>Tags</b>: {tags_str}<br>"
                f"<b>Original File</b>: {original_file_name}<br>"
                f"<b>Archived File</b>: {archived_file_name}<br>"
                f"</li>"
            )
        except Exception as e:
            print(f"Error processing document ID {doc.get('id', 'unknown')}: {e}")
            continue

    if not lines:
        lines.append("<li>No documents found.</li>")

    html_body = f"""
<html>
  <body>
    <p>Here are your documents:</p>
    <ul>
      {''.join(lines)}
    </ul>
    <p>Your trusted PaperlessNGX Runner</p>
  </body>
</html>
"""

    subject_with_count = f"{SUBJECT} ({len(docs)})"

    msg = MIMEMultipart("alternative")
    msg["Subject"] = subject_with_count
    msg["From"] = FROM
    if isinstance(TO, list):
        msg["To"] = ", ".join(TO)
    else:
        msg["To"] = TO

    part = MIMEText(html_body, "html")
    msg.attach(part)

    return msg

def send_email(msg):
    try:
        with smtplib.SMTP("localhost", 25) as server:
            server.send_message(msg)
    except Exception as e:
        print(f"Error sending email: {e}")

if __name__ == "__main__":
    try:
        correspondents = get_correspondents()
        tag_map = get_tags_map()
        docs = get_documents()
        email_msg = create_email(docs, correspondents, tag_map)
        send_email(email_msg)
        print("Email sent.")
    except Exception as e:
        print(f"Error during execution: {e}")
