// Function to load article data
async function loadArticle(articleId) {
    try {
        const response = await fetch(`articles/${articleId}.json`);
        if (!response.ok) throw new Error('Article not found');
        
        const article = await response.json();
        displayArticle(article);
        
        // Update page title
        document.title = article.title + " - Your Site Name";
        
        // For the #google_vignette part (if using ads)
        window.location.hash = "google_vignette";
        
    } catch (error) {
        document.getElementById('article-container').innerHTML = `
            <div class="error">Article not found</div>
        `;
    }
}

// Function to display the article
function displayArticle(article) {
    const container = document.getElementById('article-container');
    container.innerHTML = `
        <article class="full-article">
            <h1>${escapeHtml(article.title)}</h1>
            <div class="article-meta">Published on ${article.publish_date}</div>
            <img src="${article.image_url}" alt="${escapeHtml(article.title)}" class="article-image">
            <div class="article-content">
                ${article.full_content}
            </div>
        </article>
        
        <!-- Ad container (for google_vignette) -->
        <div id="ad-container" class="ad-unit"></div>
        
        <!-- Social sharing -->
        <div class="social-share">
            <a href="https://www.facebook.com/sharer/sharer.php?u=${encodeURIComponent(window.location.href)}" target="_blank">Share on Facebook</a>
            <a href="https://twitter.com/intent/tweet?url=${encodeURIComponent(window.location.href)}&text=${encodeURIComponent(article.title)}" target="_blank">Share on Twitter</a>
        </div>
    `;
    
    // Load ads if needed
    if (window.loadAds) {
        window.loadAds();
    }
}

// Helper function to escape HTML
function escapeHtml(unsafe) {
    return unsafe
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#039;");
}
// Handle hash-based navigation
window.addEventListener('hashchange', handleHash);
window.addEventListener('load', handleHash);

function handleHash() {
    const match = window.location.hash.match(/^#show\/(\d+)/);
    if (match) {
        const articleId = match[1];
        loadArticle(articleId);
        
        // Update the URL without reload (show.html?id=XXX)
        history.replaceState(null, null, `show.html?id=${articleId}#google_vignette`);
    }
}
