function extractArticleId(url) {
    const match = url.match(/(\d+)/);
    return match ? match[1] : null;
}

function loadNews() {
    fetch('/data/news.json')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('news-container');
            const archiveContainer = document.getElementById('archive-container');
            container.innerHTML = '';
            
            // Load first 150 articles (new news)
            const newsItems = data.articles.slice(0, 150);
            
            // Load archived news if available
            const archivedNews = JSON.parse(localStorage.getItem('archivedNews') || [];
            
            // Display archived news in the archive column
            if (archiveContainer) {
                archiveContainer.innerHTML = archivedNews.map(article => {
                    const articleId = extractArticleId(article.url);
                    const internalUrl = articleId ? `https://sahaafa.net/show${articleId}.html` : article.url;
                    
                    return `
                        <div class="news-item archive-item">
                            <h4>${article.title}</h4>
                            <div class="meta">
                                <span class="source">${article.source}</span>
                                <span class="date">${new Date(article.date).toLocaleString('ar-EG')}</span>
                            </div>
                        </div>
                    `;
                }).join('');
                
                // Add click event to archive items
                document.querySelectorAll('.archive-item').forEach(item => {
                    const article = archivedNews[item.dataset.index];
                    item.addEventListener('click', () => {
                        const articleId = extractArticleId(article.url);
                        const internalUrl = articleId ? `https://sahaafa.net/show${articleId}.html` : article.url;
                        window.location.href = internalUrl;
                    });
                });
            }
            
            // Display current news in main container
            newsItems.forEach(article => {
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
            const newArticles = newsItems.filter(newArticle => 
                !archivedNews.some(oldArticle => oldArticle.url === newArticle.url)
            );
            
            if (newArticles.length > 0) {
                const updatedArchive = [...newArticles, ...archivedNews];
                // Keep only the last 500 archived items to prevent localStorage overflow
                localStorage.setItem('archivedNews', JSON.stringify(updatedArchive.slice(0, 500)));
            }
        })
        .catch(error => {
            console.error('Error loading news:', error);
            const container = document.getElementById('news-container');
            container.innerHTML = '<div class="error">فشل تحميل الأخبار. الرجاء المحاولة لاحقًا.</div>';
        });
}
