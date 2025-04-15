import feedparser
import pandas as pd
import time

CSV_FILE = "medium_articles.csv"

def scrape_medium_rss():
    url = "https://medium.com/feed/tag/android-development"
    feed = feedparser.parse(url)

    articles = [{"link": entry.link} for entry in feed.entries]
    return articles

def save_to_csv(new_articles):
    try:
        df_existing = pd.read_csv(CSV_FILE)
    except FileNotFoundError:
        df_existing = pd.DataFrame(columns=["link"])

    df_new = pd.DataFrame(new_articles)

    df_combined = pd.concat([df_existing, df_new]).drop_duplicates(subset=["link"]).reset_index(drop=True)

    df_combined.to_csv(CSV_FILE, index=False, encoding="utf-8")
    print(f"Saved {len(df_combined)} articles to {CSV_FILE}")

if __name__ == "__main__":
    articles = scrape_medium_rss()
    if articles:
        save_to_csv(articles)
    else:
        print("No new articles found.")