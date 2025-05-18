function extractArticleId(url) {
    const match = url.match(/(\d+)/);
    return match ? match[1] : null;
}

// Load news from localStorage or initialize empty array
function getArchivedNews() {
    try {
        return JSON.parse(localStorage.getItem('archivedNews')) || [];
    } catch (e) {
        return [];
    }
}

function saveArchivedNews(articles) {
    // Keep only the last 500 articles to prevent localStorage overflow
    const limitedArticles = articles.slice(0, 500);
    localStorage.setItem('archivedNews', JSON.stringify(limitedArticles));
}

function loadNews() {
    fetch('/data/news.json')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('news-container');
            const archiveContainer = document.getElementById('archive-container');
            
            // Clear containers
            container.innerHTML = '';
            archiveContainer.innerHTML = '<h2>الأرشيف</h2>';
            
            // Get current and archived news
            const currentNews = data.articles.slice(0, 150);
            let archivedNews = getArchivedNews();

            // Display current news in main container
            currentNews.forEach(article => {
                const item = document.createElement('div');
                item.className = 'news-item';
                
                const articleId = extractArticleId(article.url);
                const internalUrl = articleId ? `https://sahaafa.net/show${articleId}.html` : article.url;
                
                item.innerHTML = `
                    <h3>${article.title}</h3>
                    <div class="meta">
                        <span class="source">${article.source}</span>
                        <span class="date">${new Date(article.date).toLocaleString('ar-EG')}</span>
                    </div>
                `;
                item.addEventListener('click', () => {
                    window.location.href = internalUrl;
                });
                container.appendChild(item);
            });

            // Archive current news if not already archived
            const newArticles = currentNews.filter(newArticle => 
                !archivedNews.some(oldArticle => oldArticle.url === newArticle.url)
            );
            
            if (newArticles.length > 0) {
                archivedNews = [...newArticles, ...archivedNews];
                saveArchivedNews(archivedNews);
            }

            // Display archived news
            archivedNews.forEach((article, index) => {
                const archiveItem = document.createElement('div');
                archiveItem.className = 'archive-item';
                archiveItem.setAttribute('data-index', index);
                
                const articleId = extractArticleId(article.url);
                const internalUrl = articleId ? `https://sahaafa.net/show${articleId}.html` : article.url;
                
                archiveItem.innerHTML = `
                    <h4>${article.title}</h4>
                    <div class="meta">
                        <span class="source">${article.source}</span>
                        <span class="date">${new Date(article.date).toLocaleString('ar-EG')}</span>
                    </div>
                `;
                
                archiveItem.addEventListener('click', () => {
                    window.location.href = internalUrl;
                });
                
                archiveContainer.appendChild(archiveItem);
            });

            // Update breaking news ticker if needed
            if (typeof updateBreakingNews === 'function') {
                updateBreakingNews();
            }
        })
        .catch(error => {
            console.error('Error loading news:', error);
            const container = document.getElementById('news-container');
            container.innerHTML = '<div class="error">فشل تحميل الأخبار. الرجاء المحاولة لاحقًا.</div>';
        });
}

// Initialize news loading when DOM is ready
document.addEventListener('DOMContentLoaded', function() {
    // Set current year in footer
    document.getElementById('current-year').textContent = new Date().getFullYear();
    
    // Load news
    loadNews();
    
    // Set up periodic refresh (every 5 minutes)
    setInterval(loadNews, 300000);
});
