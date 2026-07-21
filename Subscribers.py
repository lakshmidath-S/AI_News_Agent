import requests
import csv
import io

# Public, read-only CSV link from Google Sheets (File > Share > Publish to web > CSV)
SHEET_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSu2LK1jTW_hkszTK65x6AQbSTowyciDGRi8AUQgNt0fn-mTCtKJUcSy7aM3c8Zk3pE1BjoAbMBZL6R/pub?gid=1011871837&single=true&output=csv"


def get_subscriber_emails():
    """Fetch the current list of subscriber emails from the Google Sheet."""
    response = requests.get(SHEET_CSV_URL, timeout=15)
    response.raise_for_status()

    reader = csv.reader(io.StringIO(response.text))
    rows = list(reader)

    if not rows:
        return []

    header = rows[0]
    # find whichever column looks like the email column
    email_col_index = None
    for i, col_name in enumerate(header):
        if "email" in col_name.lower():
            email_col_index = i
            break

    if email_col_index is None:
        print("Could not find an email column in the sheet.")
        return []

    emails = []
    for row in rows[1:]:
        if len(row) > email_col_index:
            addr = row[email_col_index].strip()
            if addr:
                emails.append(addr)

    return emails


if __name__ == "__main__":
    emails = get_subscriber_emails()
    print(f"Found {len(emails)} subscriber(s):")
    for e in emails:
        print(" -", e)