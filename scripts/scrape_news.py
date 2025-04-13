import feedparser
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests

rss_feeds = [
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
    "https://alsahwa-yemen.net/feed"
]

non_rss_sites = {
    "aljazeera": "https://www.aljazeera.net/",
    "france24": "https://www.france24.com/ar/",
    "sahafah": "https://sahaafa.net/",
    "sa24": "https://sa24.co/",
    "awraqpress": "https://www.awraqpress.net/portal/",
    "methaq": "https://almethaq.net/news/"
}

articles = []

def parse_rss(url):
    try:
        feed = feedparser.parse(url)
        for entry in feed.entries[:20]:
            articles.append({
                "title": BeautifulSoup(entry.title, "html.parser").get_text(),
                "url": entry.link,
                "source": url.split("//")[1].split("/")[0],
                "date": datetime.utcnow().isoformat() + "Z"
            })
    except Exception as e:
        print(f"Error parsing RSS feed {url}: {e}")

def scrape_site(url, site_key):
    try:
        headers = {"User-Agent": "Mozilla/5.0"}
        response = requests.get(url, headers=headers, timeout=10)
        soup = BeautifulSoup(response.text, "html.parser")
        links = soup.find_all("a", href=True)
        count = 0
        for link in links:
            href = link["href"]
            text = link.get_text(strip=True)
            if len(text) >= 15 and "http" in href and site_key in href and count < 10:
                articles.append({
                    "title": text,
                    "url": href,
                    "source": site_key,
                    "date": datetime.utcnow().isoformat() + "Z"
                })
                count += 1
    except Exception as e:
        print(f"Error scraping {url}: {e}")

# Fetch from RSS feeds
for feed_url in rss_feeds:
    parse_rss(feed_url)

# Scrape from non-RSS sites
for key, site_url in non_rss_sites.items():
    scrape_site(site_url, key)

# Save to JSON
with open('data/news.json', 'w', encoding='utf-8') as f:
    json.dump({
        "lastUpdated": datetime.utcnow().isoformat() + "Z",
        "articles": articles[:200]  # Keep top 200
    }, f, ensure_ascii=False, indent=2)
