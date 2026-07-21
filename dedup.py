import json
import os

SEEN_FILE = "seen_articles.json"


def load_seen_links():
    """Load the set of article links already processed."""
    if not os.path.exists(SEEN_FILE):
        return set()
    with open(SEEN_FILE, "r") as f:
        return set(json.load(f))


def save_seen_links(seen_links):
    """Persist the set of seen article links to disk."""
    with open(SEEN_FILE, "w") as f:
        json.dump(list(seen_links), f, indent=2)


def filter_new_articles(articles, seen_links):
    """Return only articles whose link hasn't been seen before."""
    return [a for a in articles if a["link"] not in seen_links]