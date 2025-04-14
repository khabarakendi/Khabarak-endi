import json
from datetime import datetime
import feedparser
import requests
from bs4 import BeautifulSoup
import traceback

# Add these headers for all requests
HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'ar-YE,ar;q=0.9',
    'Referer': 'https://www.google.com/'
}

SOURCES = [
    # Your existing SOURCES list goes here (keep all the same sources)
    # Just make sure it starts with [ and ends with ]
    # ... paste all your current sources exactly as they are ...
]

def fetch_rss(url, source_name, category):
    """Fetch news from RSS feed (unchanged from your original)"""
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries[:15]:
            try:
                articles.append({
                    "title": entry.get('title', 'لا يوجد عنوان'),
                    "link": entry.get('link', '#'),
                    "source": source_name,
                    "time": entry.get('published', datetime.now().strftime("%H:%M")),
                    "category": category,
                    "image": entry.get('media_content', [{}])[0].get('url', '') if 'media_content' in entry else ''
                })
            except Exception as e:
                print(f"Error parsing RSS item from {source_name}: {str(e)}")
                continue
        return articles
    except Exception as e:
        print(f"Error fetching {source_name} RSS: {str(e)}")
        return []

def fetch_html(url, config):
    """Improved HTML fetcher with more debugging"""
    try:
        print(f"\n🔍 Attempting to scrape: {config['name']}")
        print(f"   URL: {url}")
        
        response = requests.get(url, headers=HEADERS, timeout=15)
        response.encoding = 'utf-8'
        print(f"   Status Code: {response.status_code}")
        
        if response.status_code != 200:
            print(f"   ❌ Bad response from server")
            return []
        
        soup = BeautifulSoup(response.text, 'html.parser')
        article_containers = soup.select(config['selectors']['articles'])
        print(f"   Found {len(article_containers)} potential articles")
        
        articles = []
        for item in article_containers[:15]:
            try:
                title = item.select_one(config['selectors']['title']).text.strip()
                link = item.select_one(config['selectors']['link'])['href']
                
                if not link.startswith('http'):
                    base_url = url.split('/')[0] + '//' + url.split('/')[2]
                    link = base_url + link if link.startswith('/') else base_url + '/' + link
                
                image = item.select_one('img')['src'] if item.select_one('img') else ''
                
                articles.append({
                    "title": title,
                    "link": link,
                    "source": config['name'],
                    "time": datetime.now().strftime("%H:%M"),
                    "category": config['category'],
                    "image": image
                })
            except Exception as e:
                print(f"   ⚠️ Failed to parse article: {str(e)}")
                continue
                
        return articles
    except Exception as e:
        print(f"   🔥 Critical scraping error: {str(e)}")
        print(traceback.format_exc())
        return []

def main():
    print("🚀 Starting news source diagnostic...")
    all_articles = []
    source_report = {}
    
    for source in SOURCES:
        try:
            print(f"\n=== Processing: {source['name']} ===")
            if source["type"] == "rss":
                articles = fetch_rss(source["url"], source["name"], source["category"])
            else:
                articles = fetch_html(source["url"], source)
            
            if articles:
                print(f"✅ Success: Got {len(articles)} articles")
                source_report[source['name']] = f"Success ({len(articles)} articles)"
                all_articles.extend(articles)
            else:
                print(f"❌ Failed: No articles retrieved")
                source_report[source['name']] = "Failed (no articles)"
                
        except Exception as e:
           
