/**
 * Loads and displays news articles
 */
function loadNews() {
    const newsContainer = document.getElementById('news-container');
    newsContainer.innerHTML = '<div class="loading"><div class="spinner"></div><p>جاري تحميل الأخبار اليمنية...</p></div>';

    fetch('data/news.json')
        .then(response => response.json())
        .then(data => {
            newsContainer.innerHTML = '';
            
            // Sort by date (newest first)
            const sortedArticles = data.articles.sort((a, b) => 
                new Date(b.date) - new Date(a.date)
            ).slice(0, 150); // Limit to 150 articles

            sortedArticles.forEach(article => {
                const timeAgo = formatTimeAgo(new Date(article.date));
                
                const articleEl = document.createElement('div');
                articleEl.className = 'news-article';
                articleEl.innerHTML = `
                    <h2 onclick="viewArticle('${article.url}', '${escapeHtml(article.title)}', '${escapeHtml(article.source)}', '${timeAgo}')">
                        ${article.title}
                    </h2>
                    <div class="article-meta">
                        <span class="source">${article.source}</span>
                        <span class="time">${timeAgo}</span>
                    </div>
                    <p>${article.summary}</p>
                    <div class="article-meta">
                        <span class="category ${article.category}">${article.category}</span>
                        <span class="date">${new Date(article.date).toLocaleDateString('ar-EG')}</span>
                    </div>
                `;
                newsContainer.appendChild(articleEl);
            });

            updateBreakingNews();
            initPagination();
        })
        .catch(error => {
            newsContainer.innerHTML = '<p class="error">حدث خطأ أثناء تحميل الأخبار. يرجى المحاولة لاحقاً.</p>';
            console.error('Error loading news:', error);
        });
}

function formatTimeAgo(date) {
    const now = new Date();
    const diffMinutes = Math.floor((now - date) / (1000 * 60));
    const hours = Math.floor(diffMinutes / 60);
    const minutes = diffMinutes % 60;
    
    if (hours > 0 && minutes > 0) {
        return `قبل ${hours} ساعة و ${minutes} دقيقة`;
    } else if (hours > 0) {
        return `قبل ${hours} ساعة`;
    } else {
        return `قبل ${minutes} دقيقة`;
    }
}

function escapeHtml(text) {
    return text.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// Initialize on load
document.addEventListener('DOMContentLoaded', loadNews);
