import feedparser
import json
from datetime import datetime

# List of RSS feeds
FEEDS = [
    "https://www.almashhad-alyemeni.com/feed",
    "https://yemennownews.com/feed",
    "https://www.24-post.com/feed",
    "https://www.anbaaden.com/feed",
    "https://huna-aden.com/feed",
    "https://taiztoday.net/feed",
    "https://www.lahjnews.net/feed",
    "https://almasdaronline.com/feed",
    "https://www.marebpress.net/feed",
    "https://www.yemeneconomist.com/feed",
    "https://yemen-press.net/feed",
    "https://alsahwa-yemen.net/feed",
    "https://www.aljazeera.net/",
    "https://www.france24.com/ar/",
    "https://sahaafa.net/",
    "https://sa24.co/",
    "https://www.awraqpress.net/portal/",
    "https://almethaq.net/news/"
]

articles = []

for feed_url in FEEDS:
    try:
        feed = feedparser.parse(feed_url)
        source_name = feed.feed.get('title') or feed_url.split("//")[1].split("/")[0]

        for entry in feed.entries[:50]:  # Limit to 50 articles per source
            pub_date = entry.get("published", datetime.utcnow().isoformat() + "Z")

            articles.append({
                "title": entry.get("title", "No Title"),
                "url": entry.get("link", ""),
                "source": source_name,
                "date": pub_date
            })

    except Exception as e:
        print(f"Failed to parse {feed_url}: {e}")

# Save to JSON file
output_data = {
    "lastUpdated": datetime.utcnow().isoformat() + "Z",
    "articles": articles
}

with open('data/news.json', 'w', encoding='utf-8') as f:
    json.dump(output_data, f, ensure_ascii=False, indent=2)

print("News data updated successfully.")
