import json
import requests
from bs4 import BeautifulSoup
from datetime import datetime

# Yemeni news sources to scrape
SOURCES = [
    {
        'name': 'المشهد اليمني',
        'url': 'https://www.almashhad-alyemeni.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.article-item',
            'title': 'h2 a',
            'link': 'h2 a',
            'time': 'span.time'
        }
    },
    {  
        'name': 'اليمن العربي',
        'url': 'https://www.yemen-arabic.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'صحافة نت',
        'url': 'https://www.sahafah.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'شبكة المهرة الاخبارية',
        'url': 'https://almahranews.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    { 
        'name': 'المهرية نت',
        'url': 'https://almahriah.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'بوست 24',
        'url': 'https://www.24-post.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'أنباء عدن',
        'url': 'https://www.anbaaden.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'هنا عدن',
        'url': 'https://huna-aden.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'تعز اليوم',
        'url': 'https://taiztoday.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'لحج نيوز',
        'url': 'https://www.lahjnews.net/news/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'المصدر أونلاين',
        'url': 'https://almasdaronline.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'مارب برس',
        'url': 'https://www.marebpress.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'الإقتصادري اليمني',
        'url': 'https://www.yemeneconomist.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'يمن برس',
        'url': 'https://yemen-press.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'الصحوة نت',
        'url': 'https://alsahwa-yemen.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'الجزيرة نت',
        'url': 'https://www.aljazeera.net/',
        'category': 'international',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'صحافة 24',
        'url': 'https://sa24.co/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'أوراق برس',
        'url': 'https://www.awraqpress.net/portal/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'هنا عدن',
        'url': 'https://huna-aden.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'اليمثاق نت',
        'url': 'https://almethaq.net/news/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
                     {
        'name': 'سبأ نيوز',
        'url': 'https://www.saba.ye/ar',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': ' هنا عدن',
        'url': 'https://huna-aden.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'أنباء يمنية',
        'url': 'https://www.yemeninews.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'الامناء نت',
        'url': 'https://al-omana.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'وكالة خبر للانباء',
        'url': 'https://khabaragency.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'البعث نيوز',
        'url': 'https://albaath-ye.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'اب نيوز',
        'url': 'https://www.ibb-news.com/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'الضالع نت',
        'url': 'https://www.dhala.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'سبتمبر26',
        'url': 'https://www.26sep.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'صحيفة الثورة',
        'url': 'https://althawrah.ye/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'عدن الغد',
        'url': 'https://www.adngad.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'كريتر نيوز',
        'url': 'https://crater-news.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
    {
        'name': 'كريبتر سكاي',
        'url': 'https://crater-sky.net/',
        'category': 'local',
        'selectors': {
            'articles': 'div.news-box',
            'title': 'h3 a',
            'link': 'h3 a',
            'time': 'span.date'
        }
    },
]

def scrape_news():
    all_articles = []
    
    for source in SOURCES:
        try:
            response = requests.get(source['url'], timeout=10)
            soup = BeautifulSoup(response.text, 'html.parser')
            articles = soup.select(source['selectors']['articles'])
            
            for article in articles[:30]:  # Get 30 articles per source
                try:
                    title = article.select_one(source['selectors']['title']).text.strip()
                    url = article.select_one(source['selectors']['link'])['href']
                    
                    # Make sure URL is absolute
                    if not url.startswith('http'):
                        url = source['url'] + url.lstrip('/')
                    
                    # Get or estimate publish time
                    time_element = article.select_one(source['selectors']['time'])
                    pub_time = time_element.text.strip() if time_element else datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
                    
                    all_articles.append({
                        'title': title,
                        'source': source['name'],
                        'date': pub_time,
                        'url': url,
                        'category': source['category']
                    })
                except Exception as e:
                    print(f"Error processing article: {e}")
                    continue
                    
        except Exception as e:
            print(f"Error scraping {source['name']}: {e}")
            continue
    
    # Save to JSON
    with open('data/news.json', 'w', encoding='utf-8') as f:
        json.dump({'articles': all_articles}, f, ensure_ascii=False, indent=2)
    
    print(f"Successfully scraped {len(all_articles)} articles")

if __name__ == '__main__':
    scrape_news()
