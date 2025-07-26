

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

// Language translations
const translations = {
    'so': {
        'title': 'Ku Soo Dhawoow Fadal Rewards 🎁',
        'description': 'Waxaan kuu haynaa fursado dhab ah oo aad online ku kasban karto adigoo aan wax lacag ah bixin. Website-kan wuxuu kuu sheegi doonaa sirta iyo siyaabaha ugu fudud ee lacag lagu helo adigoo adeegsanaya mobaylkaaga.',
        'feature1': '✅ Sidee lacag looga helo Internet-ka 2025',
        'feature2': '✅ Barnaamijyada lacag bixiya',
        'feature3': '✅ Tilmaamo sir ah',
        'feature4': '✅ Linkyo lacag kuu soo jiidaya',
        'cta': '👉 HALKAN GUJI si aad u bilowdo safarkaaga lacag-helidda!',
        'visitors': '👥 Dadka soo booqday:',
        'follow': '🔔 Nala Soco Social Media',
        'home': 'Home',
        'about': 'About Us',
        'contact': 'Contact',
        'terms': 'Terms',
        'disclaimer': 'Disclaimer'
    },
    'en': {
        'title': 'Welcome to Fadal Rewards 🎁',
        'description': 'We offer you real opportunities to earn money online without spending any money. This website will tell you the secrets and easiest ways to make money using your mobile phone.',
        'feature1': '✅ How to make money from the Internet 2025',
        'feature2': '✅ Money-paying programs',
        'feature3': '✅ Secret tips',
        'feature4': '✅ Links that bring you money',
        'cta': '👉 CLICK HERE to start your money-making journey!',
        'visitors': '👥 Visitors:',
        'follow': '🔔 Follow Us on Social Media',
        'home': 'Home',
        'about': 'About Us',
        'contact': 'Contact',
        'terms': 'Terms',
        'disclaimer': 'Disclaimer'
    },
    'ar': {
        'title': 'أهلاً بكم في مكافآت فضل 🎁',
        'description': 'نقدم لكم فرصاً حقيقية لكسب المال عبر الإنترنت دون إنفاق أي أموال. سيخبركم هذا الموقع بالأسرار والطرق الأسهل لكسب المال باستخدام هاتفكم المحمول.',
        'feature1': '✅ كيفية كسب المال من الإنترنت 2025',
        'feature2': '✅ البرامج التي تدفع المال',
        'feature3': '✅ نصائح سرية',
        'feature4': '✅ روابط تجلب لك المال',
        'cta': '👉 انقر هنا لبدء رحلة كسب المال!',
        'visitors': '👥 الزوار:',
        'follow': '🔔 تابعونا على وسائل التواصل',
        'home': 'الرئيسية',
        'about': 'من نحن',
        'contact': 'اتصل بنا',
        'terms': 'الشروط',
        'disclaimer': 'إخلاء المسؤولية'
    }
};

// Language switcher functionality
function initLanguageSelector() {
    const selector = document.getElementById('language-selector');
    if (selector) {
        // Load saved language or default to Somali
        const savedLang = localStorage.getItem('selectedLanguage') || 'so';
        selector.value = savedLang;
        changeLanguage(savedLang);
        
        selector.addEventListener('change', function() {
            const selectedLang = this.value;
            localStorage.setItem('selectedLanguage', selectedLang);
            changeLanguage(selectedLang);
        });
    }
}

// Change language function
function changeLanguage(lang) {
    const translation = translations[lang];
    if (!translation) return;
    
    // Update page content
    const elements = {
        '.hero-title': 'title',
        '.hero-description': 'description',
        '.features-list li:nth-child(1)': 'feature1',
        '.features-list li:nth-child(2)': 'feature2',
        '.features-list li:nth-child(3)': 'feature3',
        '.features-list li:nth-child(4)': 'feature4',
        '.cta-button': 'cta',
        '.visitor-counter p': 'visitors',
        '.social-buttons h3': 'follow'
    };
    
    Object.entries(elements).forEach(([selector, key]) => {
        const element = document.querySelector(selector);
        if (element && translation[key]) {
            if (selector === '.visitor-counter p') {
                const visitorCount = document.getElementById('visitor-count').textContent;
                element.innerHTML = `${translation[key]} <strong id="visitor-count">${visitorCount}</strong>`;
            } else {
                element.textContent = translation[key];
            }
        }
    });
    
    // Update navigation links
    const navLinks = document.querySelectorAll('.nav-link');
    const navTranslations = ['home', 'about', 'contact', 'terms', 'disclaimer'];
    navLinks.forEach((link, index) => {
        if (navTranslations[index] && translation[navTranslations[index]]) {
            link.textContent = translation[navTranslations[index]];
        }
    });
    
    // Update document language attribute
    document.documentElement.lang = lang;
}

// Initialize language selector when page loads
document.addEventListener('DOMContentLoaded', function() {
    // ... existing code ...
    
    // Initialize language selector
    initLanguageSelector();
});
