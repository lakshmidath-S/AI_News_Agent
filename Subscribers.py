import requests
import csv
import io

# Public, read-only CSV links from Google Sheets (File > Share > Publish to web > CSV)
SUBSCRIBE_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vSu2LK1jTW_hkszTK65x6AQbSTowyciDGRi8AUQgNt0fn-mTCtKJUcSy7aM3c8Zk3pE1BjoAbMBZL6R/pub?gid=1011871837&single=true&output=csv"

# Set this after creating a second Google Form for unsubscribes and publishing it the same way
UNSUBSCRIBE_CSV_URL = "https://docs.google.com/spreadsheets/d/e/2PACX-1vRlyuURwQkBCC9fwAl3PtpbMjntspQscGGx6l4kUyq4_SOIFIqF5GuiFFfXFzY4MVFx4byfmpfD-ujk/pub?gid=744171298&single=true&output=csv"


def _extract_emails_from_csv(csv_url):
    if not csv_url:
        return set()

    response = requests.get(csv_url, timeout=15)
    response.raise_for_status()

    reader = csv.reader(io.StringIO(response.text))
    rows = list(reader)

    if not rows:
        return set()

    header = rows[0]
    email_col_index = None
    for i, col_name in enumerate(header):
        if "email" in col_name.lower():
            email_col_index = i
            break

    if email_col_index is None:
        return set()

    emails = set()
    for row in rows[1:]:
        if len(row) > email_col_index:
            addr = row[email_col_index].strip().lower()
            if addr:
                emails.add(addr)

    return emails


def get_subscriber_emails():
    """Fetch the current list of subscriber emails, excluding anyone who unsubscribed."""
    subscribed = _extract_emails_from_csv(SUBSCRIBE_CSV_URL)
    unsubscribed = _extract_emails_from_csv(UNSUBSCRIBE_CSV_URL)

    active = subscribed - unsubscribed
    return list(active)


if __name__ == "__main__":
    emails = get_subscriber_emails()
    print(f"Found {len(emails)} active subscriber(s):")
    for e in emails:
        print(" -", e)