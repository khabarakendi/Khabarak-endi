// This ensures the google_vignette anchor is always present
document.addEventListener('DOMContentLoaded', function() {
    if (window.location.pathname.includes('show') && !window.location.hash) {
        window.location.hash = 'google_vignette';
    }
    
    // Initialize ads (if you're using AdSense)
    if (typeof adsbygoogle !== 'undefined') {
        (adsbygoogle = window.adsbygoogle || []).push({});
    }
});
