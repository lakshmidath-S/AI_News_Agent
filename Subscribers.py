import os
import requests
import csv
import io

# Required environment variables:
#   SUBSCRIBE_CSV_URL   - published CSV link for the subscribe Google Form/Sheet
#   UNSUBSCRIBE_CSV_URL - published CSV link for the unsubscribe Google Form/Sheet (optional)


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
    subscribe_url = os.environ.get("SUBSCRIBE_CSV_URL", "")
    unsubscribe_url = os.environ.get("UNSUBSCRIBE_CSV_URL", "")

    subscribed = _extract_emails_from_csv(subscribe_url)
    unsubscribed = _extract_emails_from_csv(unsubscribe_url)

    active = subscribed - unsubscribed
    return list(active)


if __name__ == "__main__":
    emails = get_subscriber_emails()
    print(f"Found {len(emails)} active subscriber(s):")
    for e in emails:
        print(" -", e)