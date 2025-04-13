function loadNews() {
    fetch('/data/news.json')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('news-container');
            container.innerHTML = '';

            // Remove slice limitation to show all articles (100+)
            const newsItems = data.articles.sort((a, b) => 
                new Date(b.date) - new Date(a.date)
            );

            newsItems.forEach(article => {
                const item = document.createElement('div');
                item.className = 'news-item';
                
                // Format time as "قبل X ساعة و Y دقيقة"
                const timeAgo = formatTimeAgo(new Date(article.date));
                
                item.innerHTML = `
                    <h3 onclick="viewArticle('${article.url}', '${escapeHtml(article.title)}', '${escapeHtml(article.source)}', '${timeAgo}')">
                        ${article.title}
                    </h3>
                    <div class="meta">
                        <span class="source">${article.source}</span>
                        <span class="time">${timeAgo}</span>
                    </div>
                    <div class="category ${article.category}">${getCategoryName(article.category)}</div>
                `;
                container.appendChild(item);
            });

            // Initialize pagination for all articles
            initPagination(newsItems.length);
            
            // Update breaking news ticker
            updateBreakingNews();
        })
        .catch(error => {
            console.error('Error loading news:', error);
            const container = document.getElementById('news-container');
            container.innerHTML = '<div class="error">فشل تحميل الأخبار. الرجاء المحاولة لاحقًا.</div>';
        });
}

// Helper function to format time as "قبل X ساعة و Y دقيقة"
function formatTimeAgo(date) {
    const now = new Date();
    const diffMinutes = Math.floor((now - date) / (1000 * 60));
    const hours = Math.floor(diffMinutes / 60);
    const minutes = diffMinutes % 60;
    
    if (hours > 0 && minutes > 0) {
        return `قبل ${hours} ساعة و ${minutes} دقيقة`;
    } else if (hours > 0) {
        return `قبل ${hours} ساعة`;
    } else if (minutes > 0) {
        return `قبل ${minutes} دقيقة`;
    } else {
        return 'الآن';
    }
}

// Helper function to escape HTML
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML.replace(/"/g, '&quot;').replace(/'/g, '&#39;');
}

// Helper function to get category name
function getCategoryName(category) {
    const categories = {
        'local': 'محلية',
        'international': 'دولية',
        'sports': 'رياضة',
        'economic': 'اقتصادية',
        'private': 'خاصة'
    };
    return categories[category] || category;
}

// Initialize on page load
document.addEventListener('DOMContentLoaded', loadNews);
