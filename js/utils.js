/**
 * Utility functions
 */

// Update current datetime
function updateDateTime() {
    const now = new Date();
    const options = {
        weekday: 'long',
        year: 'numeric',
        month: 'long',
        day: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    };
    const dateStr = now.toLocaleDateString('ar-EG', options)
        .replace(/،/g, ' - ')
        .replace(/ص/g, 'ص')
        .replace(/م/g, 'م');

    document.getElementById('current-datetime').textContent = dateStr;
}

// Update breaking news ticker with latest 3 articles
function updateBreakingNews() {
    const articles = document.querySelectorAll('.news-article');
    const ticker = document.getElementById('breaking-news-ticker');
    
    if (articles.length >= 3) {
        const latestArticles = Array.from(articles).slice(0, 3);
        ticker.innerHTML = latestArticles.map(article => {
            const title = article.querySelector('h2').textContent;
            const onclick = article.querySelector('h2').getAttribute('onclick');
            const url = onclick.match(/viewArticle\('([^']+)'/)[1];
            const source = article.querySelector('.source').textContent;
            const time = article.querySelector('.time').textContent;
            
            return `<span class="ticker-item" onclick="viewArticle('${url}', '${title.replace(/'/g, "\\'")}', '${source}', '${time}')">• ${title} •</span>`;
        }).join('');
        
        // Restart animation
        ticker.style.animation = 'none';
        void ticker.offsetWidth;
        ticker.style.animation = 'ticker 25s linear infinite';
    }
}

// Filter news by search term
function filterNews(searchTerm) {
    const term = searchTerm.toLowerCase();
    document.querySelectorAll('.news-article').forEach(article => {
        const title = article.querySelector('h2').textContent.toLowerCase();
        const summary = article.querySelector('p').textContent.toLowerCase();
        article.style.display = (title.includes(term) || summary.includes(term)) ? 'block' : 'none';
    });
    initPagination(); // Reinitialize pagination after filtering
}

// Sort news by date
function sortNews(order) {
    const container = document.getElementById('news-container');
    const articles = Array.from(document.querySelectorAll('.news-article'));
    
    articles.sort((a, b) => {
        const aDate = new Date(a.querySelector('.date').textContent);
        const bDate = new Date(b.querySelector('.date').textContent);
        return order === 'newest' ? bDate - aDate : aDate - bDate;
    });
    
    articles.forEach(article => container.appendChild(article));
    showPage(1);
}

// Initialize all utilities
function initUtils() {
    updateDateTime();
    setInterval(updateDateTime, 60000); // Update every minute
    setInterval(updateBreakingNews, 300000); // Update breaking news every 5 minutes
    
    // Set current year in footer
    document.getElementById('current-year').textContent = new Date().getFullYear();
}

document.addEventListener('DOMContentLoaded', initUtils);
