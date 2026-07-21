import feedparser


def fetch_latest_articles(feed_url, limit=5):
    """Fetch the latest articles from an RSS feed URL."""
    feed = feedparser.parse(feed_url)
    articles = []

    for entry in feed.entries[:limit]:
        articles.append({
            "title": entry.title,
            "link": entry.link,
            "published": entry.get("published", "N/A"),
            "summary": entry.get("summary", "")
        })

    return articles