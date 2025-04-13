function updateBreakingNews() {
    const articles = document.querySelectorAll('.news-article');
    const ticker = document.getElementById('breaking-news-ticker');
    
    if (!ticker) return; // Safety check
    
    if (articles.length >= 3) {
        const latestArticles = Array.from(articles).slice(0, 3);
        ticker.innerHTML = latestArticles.map(article => {
            const title = article.querySelector('h2').textContent;
            const onclick = article.querySelector('h2').getAttribute('onclick');
            if (!onclick) return '';
            
            const urlMatch = onclick.match(/viewArticle\('([^']+)'/);
            if (!urlMatch) return '';
            
            const url = urlMatch[1];
            return `<span class="ticker-item" onclick="viewArticle('${url}')">• ${title} •</span>`;
        }).filter(item => item !== '').join('');
        
        // Restart animation
        ticker.style.animation = 'none';
        void ticker.offsetWidth;
        ticker.style.animation = 'ticker 25s linear infinite';
    } else {
        ticker.innerHTML = '<span class="ticker-item">جاري تحميل آخر الأخبار...</span>';
    }
}
