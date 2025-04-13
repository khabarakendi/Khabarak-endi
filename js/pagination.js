let currentPage = 1;
const itemsPerPage = 10;

function initPagination() {
    const articles = document.querySelectorAll('.news-article');
    const totalPages = Math.ceil(articles.length / itemsPerPage);
    const pageNumbers = document.getElementById('page-numbers');
    
    pageNumbers.innerHTML = '';
    
    for (let i = 1; i <= totalPages; i++) {
        const pageLink = document.createElement('a');
        pageLink.href = '#';
        pageLink.textContent = i;
        if (i === 1) pageLink.className = 'active';
        
        pageLink.addEventListener('click', (e) => {
            e.preventDefault();
            showPage(i);
        });
        
        pageNumbers.appendChild(pageLink);
    }
    
    showPage(1);
    updatePaginationButtons();
}

function showPage(pageNumber) {
    currentPage = pageNumber;
    const articles = document.querySelectorAll('.news-article');
    const startIndex = (pageNumber - 1) * itemsPerPage;
    const endIndex = startIndex + itemsPerPage;
    
    articles.forEach((article, index) => {
        article.style.display = (index >= startIndex && index < endIndex) ? 'block' : 'none';
    });
    
    // Update active page link
    document.querySelectorAll('.pages a').forEach(link => {
        link.classList.toggle('active', parseInt(link.textContent) === pageNumber);
    });
    
    updatePaginationButtons();
}

function updatePaginationButtons() {
    const totalPages = document.querySelectorAll('.pages a').length;
    document.querySelector('.prev').disabled = currentPage === 1;
    document.querySelector('.next').disabled = currentPage === totalPages;
}

// Event listeners
document.querySelector('.prev').addEventListener('click', () => {
    if (currentPage > 1) showPage(currentPage - 1);
});

document.querySelector('.next').addEventListener('click', () => {
    const totalPages = document.querySelectorAll('.pages a').length;
    if (currentPage < totalPages) showPage(currentPage + 1);
});
