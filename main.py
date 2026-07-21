from news_fetcher import fetch_latest_articles
from dedup import load_seen_links, save_seen_links, filter_new_articles
from summarize import summarize_article
from emailer import send_article_email

FEED_URLS = [
    "https://techcrunch.com/category/artificial-intelligence/feed/",
    "https://venturebeat.com/category/ai/feed/",
    "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
]
FETCH_LIMIT = 5


def run_pipeline():
    seen_links = load_seen_links()
    print(f"Already seen: {len(seen_links)} articles")

    all_articles = []
    for feed_url in FEED_URLS:
        all_articles.extend(fetch_latest_articles(feed_url, limit=FETCH_LIMIT))

    new_articles = filter_new_articles(all_articles, seen_links)

    print(f"Fetched: {len(all_articles)} | New: {len(new_articles)}\n")

    for i, article in enumerate(new_articles, start=1):
        print(f"--- New Article {i} ---")
        print("Title:", article["title"])
        print("Link:", article["link"])

        post_text = summarize_article(article["title"], article["summary"])
        print("\nGenerated post:")
        print(post_text)
        print(f"(Length: {len(post_text)} characters)")

        send_article_email(article["title"], post_text, article["link"])
        print("Email sent.\n")

        seen_links.add(article["link"])

    save_seen_links(seen_links)
    print("Done. Seen list updated.")


if __name__ == "__main__":
    run_pipeline()