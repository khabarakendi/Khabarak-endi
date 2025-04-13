import feedparser
import json
from datetime import datetime
from bs4 import BeautifulSoup
import requests

FEEDS = [
    'https://www.almashhad-alyemeni.com/feed',
    'https://yemennownews.com/feed',
    'https://www.24-post.com/feed',
    'https://www.anbaaden.com/feed',
    'https://huna-aden.com/feed',
    'https://taiztoday.net/feed',
    'https://www.lahjnews.net/feed',
    'https://almasdaronline.com/feed',
    'https://www.marebpress.net/feed',
    'https://www.yemeneconomist.com/feed',
    'https://yemen-press.net/feed',
    'https://alsahwa-yemen.net/feed'
]

NON_RSS_SITES = [
    {
        'name': 'Al Jazeera',
        'url': 'https://www.aljazeera.com/where/yemen/',
        'article_selector': 'div.gc__content > a',
        'title_selector': 'h3.gc__title',
        'link_attr': 'href'
    },
    {
        'name': 'France24',
        'url': 'https://www.france24.com/ar/',
        'article_selector': 'a.article__link',
        'title_selector': 'h3.article__title',
        'link_attr': 'href'
    },
    {
        'name': 'Sahaafa',
        'url': 'https://sahaafa.net/',
        'article_selector': 'div.news-item > a',
        'title_selector': 'h2.news-title',
        'link_attr': 'href'
    },
    {
        'name': 'SA24',
        'url': 'https://sa24.co/',
        'article_selector': 'div.post > a',
        'title_selector': 'h2.post-title',
        'link_attr': 'href'
    },
    {
        'name': 'AwraqPress',
        'url': 'https://www.awraqpress.net/portal/',
        'article_selector': 'div.article > a',
        'title_selector': 'h2.article-title',
        'link_attr': 'href'
    },
    {
        'name': 'Almethaq',
        'url': 'https://almethaq.net/news/',
        'article_selector': 'div.news-item > a',
        'title_selector': 'h2.news-title',
        'link_attr': 'href'
    },
    {
        'name': 'Itlobni',
        'url': 'https://itlobni.com/',
        'article_selector': 'div.news-item > a',
        'title_selector': 'h2.news-title',
        'link_attr': 'href'
    }
]

def get_feed_articles(url):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=10)
        feed = feedparser.parse(response.content)
        articles = []
        for entry in feed.entries[:30]:
            articles.append({
                'title': entry.title,
                'url': entry.link,
                'source': url,
                'date': datetime.utcnow().isoformat() + 'Z'
            })
        return articles
    except Exception as e:
        print(f'Error fetching RSS feed {url}: {str(e)}')
        return []

def scrape_site(site):
    try:
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(site['url'], headers=headers, timeout=10)
        soup = BeautifulSoup(response.content, 'html.parser')
        articles = []
        for article_tag in soup.select(site['article_selector'])[:30]:
            title_tag = article_tag.select_one(site['title_selector'])
            if title_tag:
                title = title_tag.get_text(strip=True)
                link = article_tag.get(site['link_attr'])
                if link and not link.startswith('http'):
                    link = site['url'].rstrip('/') + '/' + link.lstrip('/')
                articles.append({
                    'title': title,
                    'url': link,
                    'source': site['name'],
                    'date': datetime.utcnow().isoformat() + 'Z'
                })
        return articles
    except Exception as e:
        print(f'Error scraping site {site["name"]}: {str(e)}')
        return []

def main():
    all_articles = []

    for feed_url in FEEDS:
        all_articles.extend(get_feed_articles(feed_url))

    for site in NON_RSS_SITES:
        all_articles.extend(scrape_site(site))

    # Remove duplicates based on URL
    seen_urls = set()
    unique_articles = []
    for article in all_articles:
        if article['url'] not in seen_urls:
            seen_urls.add(article['url'])
            unique_articles.append(article)

    # Sort articles by date (most recent first)
    unique_articles.sort(key=lambda x: x['date'], reverse=True)

    # Limit to 150 articles
    final_articles = unique_articles[:150]

    with open('data/news.json', 'w', encoding='utf-8')
::contentReference[oaicite:4]{index=4}
 
