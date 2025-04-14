function loadNews() {
    fetch('/data/news.json')
        .then(response => response.json())
        .then(data => {
            const container = document.getElementById('news-container');
            container.innerHTML = '';

            const newsItems = data.articles.slice(0, 150); // Load first 150 articles

            newsItems.forEach(article => {
                const item = document.createElement('div');
                item.className = 'news-item';
                item.innerHTML = `
                    <h3>${article.title}</h3>
                    <div class="meta">
                        <span class="source">${article.source}</span>
                        <span class="date">${new Date(article.date).toLocaleString('ar-EG')}</span>
                    </div>
                `;
                item.addEventListener('click', () => viewArticle(article.url));
                container.appendChild(item);
            });
        })
        .catch(error => {
            console.error('Error loading news:', error);
            const container = document.getElementById('news-container');
            container.innerHTML = '<div class="error">فشل تحميل الأخبار. الرجاء المحاولة لاحقًا.</div>';
        });
}
