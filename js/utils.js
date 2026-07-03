/**
 * ICN Blog — Utility Functions
 * Copy code, download scripts, syntax highlighting, UI helpers
 */

// ============================================
// CODE UTILITIES
// ============================================

/**
 * Copy text to clipboard with fallback
 */
function copyToClipboard(text) {
    // Modern approach
    if (navigator.clipboard && navigator.clipboard.writeText) {
        return navigator.clipboard.writeText(text).catch(err => {
            console.error('Clipboard write failed:', err);
            return fallbackCopy(text);
        });
    }
    // Fallback for older browsers
    return fallbackCopy(text);
}

function fallbackCopy(text) {
    return new Promise((resolve, reject) => {
        const textarea = document.createElement('textarea');
        textarea.value = text;
        textarea.style.position = 'fixed';
        textarea.style.opacity = '0';
        document.body.appendChild(textarea);
        textarea.select();
        
        try {
            document.execCommand('copy');
            resolve();
        } catch (err) {
            reject(err);
        } finally {
            document.body.removeChild(textarea);
        }
    });
}

/**
 * Initialize all copy buttons on the page
 */
function initCopyButtons() {
    document.querySelectorAll('.copy-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const codeBlock = this.closest('.code-block');
            if (!codeBlock) return;
            
            const code = codeBlock.querySelector('code').textContent;
            
            copyToClipboard(code).then(() => {
                // Visual feedback
                const icon = this.querySelector('i');
                const originalClass = icon ? icon.className : '';
                
                if (icon) {
                    icon.className = 'fa-solid fa-check';
                }
                this.classList.add('copied');
                
                // Store original text for tooltip
                const originalText = this.textContent;
                this.textContent = ' Copied!';
                
                if (icon) {
                    this.prepend(icon);
                }
                
                // Reset after 2 seconds
                setTimeout(() => {
                    if (icon) {
                        icon.className = originalClass;
                    }
                    this.classList.remove('copied');
                    this.textContent = originalText;
                    if (icon) {
                        this.prepend(icon);
                    }
                }, 2000);
            }).catch(err => {
                console.error('Copy failed:', err);
            });
        });
    });
}

// ============================================
// DOWNLOAD UTILITIES
// ============================================

/**
 * Download text content as a file
 */
function downloadFile(content, filename, type = 'text/plain') {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    a.style.display = 'none';
    
    document.body.appendChild(a);
    a.click();
    
    // Cleanup
    setTimeout(() => {
        document.body.removeChild(a);
        URL.revokeObjectURL(url);
    }, 100);
}

/**
 * Initialize all download buttons on the page
 */
function initDownloadButtons() {
    document.querySelectorAll('.download-btn').forEach(btn => {
        btn.addEventListener('click', function() {
            const filename = this.dataset.filename || 'script.py';
            const code = this.dataset.code || '';
            
            if (code) {
                downloadFile(code, filename);
                
                // Visual feedback
                const originalHTML = this.innerHTML;
                this.innerHTML = '<i class="fa-solid fa-check"></i> Downloaded!';
                setTimeout(() => {
                    this.innerHTML = originalHTML;
                }, 2000);
            }
        });
    });
}

// ============================================
// PROJECT TOGGLE
// ============================================

/**
 * Initialize collapsible project cards
 */
function initProjectToggles() {
    document.querySelectorAll('.project-header').forEach(header => {
        header.addEventListener('click', function() {
            const card = this.closest('.project-card');
            const body = card.querySelector('.project-body');
            const isOpen = body.classList.contains('open');
            
            // Toggle this project
            if (isOpen) {
                body.classList.remove('open');
                this.classList.remove('open');
            } else {
                body.classList.add('open');
                this.classList.add('open');
            }
            
            // Highlight code if Prism is loaded
            if (!isOpen && typeof Prism !== 'undefined') {
                body.querySelectorAll('code').forEach(block => {
                    Prism.highlightElement(block);
                });
            }
        });
    });
}

// ============================================
// SMOOTH SCROLL
// ============================================

/**
 * Initialize smooth scrolling for anchor links
 */
function initSmoothScroll() {
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function(e) {
            const href = this.getAttribute('href');
            
            // Skip if it's just "#"
            if (href === '#') return;
            
            const target = document.querySelector(href);
            if (target) {
                e.preventDefault();
                const headerOffset = 80;
                const elementPosition = target.getBoundingClientRect().top;
                const offsetPosition = elementPosition + window.pageYOffset - headerOffset;
                
                window.scrollTo({
                    top: offsetPosition,
                    behavior: 'smooth'
                });
            }
        });
    });
}

// ============================================
// BACK TO TOP
// ============================================

/**
 * Initialize back-to-top button
 */
function initBackToTop() {
    const btn = document.getElementById('backToTop');
    if (!btn) return;
    
    window.addEventListener('scroll', () => {
        if (window.scrollY > 500) {
            btn.classList.add('visible');
        } else {
            btn.classList.remove('visible');
        }
    });
    
    btn.addEventListener('click', () => {
        window.scrollTo({ top: 0, behavior: 'smooth' });
    });
}

// ============================================
// ACTIVE NAVIGATION
// ============================================

/**
 * Highlight current page in navigation
 */
function highlightCurrentNav() {
    const currentPath = window.location.pathname;
    
    document.querySelectorAll('.nav-link, .dropdown-menu a').forEach(link => {
        const href = link.getAttribute('href');
        if (href && currentPath.endsWith(href)) {
            link.classList.add('active');
        }
    });
}

// ============================================
// SEARCH
// ============================================

/**
 * Navigate to search page with query
 */
function searchModules(query) {
    if (query && query.trim()) {
        window.location.href = `search.html?q=${encodeURIComponent(query.trim())}`;
    }
}

/**
 * Initialize search inputs
 */
function initSearchInputs() {
    // Desktop search
    const desktopInput = document.getElementById('headerSearch');
    const desktopBtn = document.getElementById('headerSearchBtn');
    
    if (desktopInput && desktopBtn) {
        desktopBtn.addEventListener('click', () => searchModules(desktopInput.value));
        desktopInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') searchModules(desktopInput.value);
        });
    }
    
    // Mobile search
    const mobileInput = document.getElementById('mobileSearchInput');
    if (mobileInput) {
        mobileInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') searchModules(mobileInput.value);
        });
    }
    
    // Search page input
    const searchPageInput = document.getElementById('searchPageInput');
    if (searchPageInput) {
        const urlParams = new URLSearchParams(window.location.search);
        const query = urlParams.get('q');
        if (query) {
            searchPageInput.value = query;
        }
        
        searchPageInput.addEventListener('keypress', (e) => {
            if (e.key === 'Enter') searchModules(searchPageInput.value);
        });
        
        const searchPageBtn = document.getElementById('searchPageBtn');
        if (searchPageBtn) {
            searchPageBtn.addEventListener('click', () => searchModules(searchPageInput.value));
        }
    }
}

// ============================================
// MOBILE MENU
// ============================================

/**
 * Initialize mobile menu toggle
 */
function initMobileMenu() {
    const menuBtn = document.getElementById('mobileMenuBtn');
    const nav = document.getElementById('mainNav');
    const mobileSearch = document.getElementById('mobileSearch');
    
    if (!menuBtn || !nav) return;
    
    menuBtn.addEventListener('click', () => {
        const isOpen = nav.classList.toggle('open');
        if (mobileSearch) {
            mobileSearch.style.display = isOpen ? 'block' : 'none';
        }
        // Update icon
        const icon = menuBtn.querySelector('i');
        if (icon) {
            icon.className = isOpen ? 'fa-solid fa-xmark' : 'fa-solid fa-bars';
        }
    });
    
    // Close menu when clicking outside
    document.addEventListener('click', (e) => {
        if (!nav.contains(e.target) && !menuBtn.contains(e.target)) {
            nav.classList.remove('open');
            if (mobileSearch) {
                mobileSearch.style.display = 'none';
            }
            const icon = menuBtn.querySelector('i');
            if (icon) {
                icon.className = 'fa-solid fa-bars';
            }
        }
    });
    
    // Mobile dropdown toggles
    document.querySelectorAll('.nav-dropdown .dropdown-toggle').forEach(toggle => {
        toggle.addEventListener('click', function(e) {
            if (window.innerWidth <= 1024) {
                e.preventDefault();
                const dropdown = this.closest('.nav-dropdown');
                const menu = dropdown.querySelector('.dropdown-menu');
                if (menu) {
                    menu.classList.toggle('open');
                }
            }
        });
    });
}

// ============================================
// ACTIVE SECTION HIGHLIGHT (Module pages)
// ============================================

/**
 * Highlight active section in table of contents
 */
function initActiveSectionHighlight() {
    const sections = document.querySelectorAll('.module-section[id]');
    const tocLinks = document.querySelectorAll('.module-toc a');
    
    if (sections.length === 0 || tocLinks.length === 0) return;
    
    window.addEventListener('scroll', () => {
        let current = '';
        const scrollPosition = window.scrollY + 120;
        
        sections.forEach(section => {
            const sectionTop = section.offsetTop;
            if (scrollPosition >= sectionTop) {
                current = section.getAttribute('id');
            }
        });
        
        tocLinks.forEach(link => {
            link.classList.remove('active');
            if (link.getAttribute('href') === '#' + current) {
                link.classList.add('active');
            }
        });
    });
}

// ============================================
// YEAR FILTER (Module listing pages)
// ============================================

/**
 * Initialize year filter buttons
 */
function initYearFilter() {
    const filterBtns = document.querySelectorAll('.filter-btn');
    const moduleCards = document.querySelectorAll('.module-card');
    
    if (filterBtns.length === 0) return;
    
    filterBtns.forEach(btn => {
        btn.addEventListener('click', function() {
            const year = this.dataset.year;
            
            // Update active button
            filterBtns.forEach(b => b.classList.remove('active'));
            this.classList.add('active');
            
            // Filter cards
            moduleCards.forEach(card => {
                if (year === 'all' || card.dataset.year === year) {
                    card.style.display = '';
                    card.style.animation = 'fadeInUp 0.3s ease forwards';
                } else {
                    card.style.display = 'none';
                }
            });
        });
    });
}

// ============================================
// STATS COUNTER ANIMATION
// ============================================

/**
 * Animate stat numbers counting up
 */
function animateStats() {
    const statNumbers = document.querySelectorAll('.stat-number[data-count]');
    
    statNumbers.forEach(stat => {
        const target = parseInt(stat.dataset.count);
        const duration = 1500;
        const start = performance.now();
        
        function update(currentTime) {
            const elapsed = currentTime - start;
            const progress = Math.min(elapsed / duration, 1);
            
            // Ease-out effect
            const eased = 1 - Math.pow(1 - progress, 3);
            const current = Math.floor(eased * target);
            
            stat.textContent = current.toLocaleString();
            
            if (progress < 1) {
                requestAnimationFrame(update);
            }
        }
        
        // Start animation when element is visible
        const observer = new IntersectionObserver((entries) => {
            entries.forEach(entry => {
                if (entry.isIntersecting) {
                    requestAnimationFrame(update);
                    observer.unobserve(entry.target);
                }
            });
        }, { threshold: 0.5 });
        
        observer.observe(stat);
    });
}

// ============================================
// INITIALIZATION
// ============================================

/**
 * Initialize all utilities when DOM is ready
 */
document.addEventListener('DOMContentLoaded', () => {
    initCopyButtons();
    initDownloadButtons();
    initProjectToggles();
    initSmoothScroll();
    initBackToTop();
    initMobileMenu();
    initSearchInputs();
    initActiveSectionHighlight();
    initYearFilter();
    highlightCurrentNav();
    animateStats();
});