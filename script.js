

// Mobile Navigation Toggle
document.addEventListener('DOMContentLoaded', function() {
    const hamburger = document.querySelector('.hamburger');
    const navMenu = document.querySelector('.nav-menu');
    
    if (hamburger && navMenu) {
        hamburger.addEventListener('click', function() {
            hamburger.classList.toggle('active');
            navMenu.classList.toggle('active');
        });
        
        // Close menu when clicking on nav links
        document.querySelectorAll('.nav-link').forEach(link => {
            link.addEventListener('click', () => {
                hamburger.classList.remove('active');
                navMenu.classList.remove('active');
            });
        });
    }
    
    // Update visitor count
    updateVisitorCount();
});

// Simple visitor counter using localStorage
function updateVisitorCount() {
    let visitors = localStorage.getItem('visitorCount') || 0;
    visitors = parseInt(visitors) + 1;
    localStorage.setItem('visitorCount', visitors);
    
    const counterElement = document.getElementById('visitor-count');
    if (counterElement) {
        counterElement.textContent = visitors;
    }
}
