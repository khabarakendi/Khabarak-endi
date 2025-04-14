import feedparser
import json
from datetime import datetime

# Define RSS feed sources
SOURCES = {
    "Otad News": "https://crater-sky.net/",
    "Hamodi News": "https://sahaafa.net/",
    "BBC Arabic": "http://www.bbc.co.uk/arabic/index.xml",
    "Al Jazeera": "https://www.aljazeera.com/xml/rss/all.xml",
    "Reuters": "https://www.reutersagency.com/feed/?best-regions=Middle-East"
}

# Fetch and process news from sources
news_articles = []
for source_name, url in SOURCES.items():
    feed = feedparser.parse(url)
    for entry in feed.entries[:10]:  # Limit to latest 10 articles per source
        article = {
            "title": entry.title,
            "url": entry.link,
            "source": source_name,
            "date": entry.published if "published" in entry else str(datetime.now())
        }
        news_articles.append(article)

# Save fetched news to JSON file
output_file = "data/news.json"
with open(output_file, "w", encoding="utf-8") as f:
    json.dump({"articles": news_articles}, f, ensure_ascii=False, indent=4)

print(f"Successfully fetched and saved {len(news_articles)} articles to {output_file}.")
