/**
 * ICN Blog — Main Application
 * Homepage rendering, module cards, filtering, and initialization
 */

// ============================================
// MODULE CARD RENDERER
// ============================================

class ModuleCardRenderer {
    constructor(containerId = 'moduleGrid') {
        this.container = document.getElementById(containerId);
        this.iconMap = {
            'programming': 'fa-code',
            'networking': 'fa-network-wired',
            'security': 'fa-shield-haltered',
            'data': 'fa-database',
            'systems': 'fa-server',
            'ai': 'fa-brain',
            'web': 'fa-globe',
            'mobile': 'fa-mobile-screen',
            'cloud': 'fa-cloud',
            'iot': 'fa-microchip',
            'forensics': 'fa-magnifying-glass',
            'hacking': 'fa-user-secret'
        };
        this.colorMap = {
            'programming': '#3fb950',
            'networking': '#58a6ff',
            'security': '#f85149',
            'data': '#d2991d',
            'systems': '#a371f7',
            'ai': '#ec4899',
            'web': '#14b8a6',
            'mobile': '#f97316',
            'cloud': '#6366f1',
            'iot': '#22c55e',
            'forensics': '#38bdf8',
            'hacking': '#ef4444'
        };
    }

    /**
     * Get icon class for module
     */
    getIcon(iconType) {
        return this.iconMap[iconType] || 'fa-book';
    }

    /**
     * Get accent color for module
     */
    getColor(iconType) {
        return this.colorMap[iconType] || '#8b949e';
    }

    /**
     * Render module cards from data array
     */
    render(modules) {
        if (!this.container) return;

        if (!modules || modules.length === 0) {
            this.showEmpty();
            return;
        }

        this.container.innerHTML = modules.map(module => this.createCard(module)).join('');
        this.attachClickHandlers();
    }

    /**
     * Create HTML for a single module card
     */
    createCard(module) {
        const icon = this.getIcon(module.icon);
        const color = this.getColor(module.icon);
        const projectCount = module.projects ? module.projects.length : 0;
        const yearLabel = module.year ? module.year.replace('year', 'Year ') : '';
        const semesterLabel = module.semesterName || '';

        return `
            <div class="module-card" 
                 data-url="${module.url || '#'}" 
                 data-year="${module.year || ''}"
                 data-tags="${(module.tags || []).join(',')}"
                 style="--card-accent: ${color};">
                
                <div class="module-card-accent" style="background: ${color};"></div>
                
                <div class="module-card-icon" style="color: ${color};">
                    <i class="fa-solid ${icon}"></i>
                </div>
                
                <div class="module-card-info">
                    <span class="module-card-code">${module.code || ''}</span>
                    <h3 class="module-card-title">${module.name}</h3>
                    <p class="module-card-desc">${this.truncate(module.description, 120)}</p>
                </div>
                
                <div class="module-card-meta">
                    <span class="meta-year">
                        <i class="fa-solid fa-calendar"></i> ${yearLabel}
                    </span>
                    <span class="meta-semester">
                        <i class="fa-solid fa-clock"></i> ${semesterLabel}
                    </span>
                </div>
                
                <div class="module-card-footer">
                    <span class="project-count">
                        <i class="fa-solid fa-code"></i>
                        ${projectCount} Project${projectCount !== 1 ? 's' : ''}
                    </span>
                    <span class="card-arrow" style="color: ${color};">
                        <i class="fa-solid fa-arrow-right"></i>
                    </span>
                </div>
            </div>
        `;
    }

    /**
     * Attach click handlers to cards
     */
    attachClickHandlers() {
        this.container.querySelectorAll('.module-card').forEach(card => {
            card.addEventListener('click', function(e) {
                // Don't navigate if user is selecting text
                if (window.getSelection().toString()) return;
                
                const url = this.dataset.url;
                if (url && url !== '#') {
                    window.location.href = url;
                }
            });

            // Keyboard accessibility
            card.setAttribute('tabindex', '0');
            card.addEventListener('keydown', function(e) {
                if (e.key === 'Enter' || e.key === ' ') {
                    e.preventDefault();
                    this.click();
                }
            });
        });
    }

    /**
     * Show empty state
     */
    showEmpty() {
        if (!this.container) return;
        
        this.container.innerHTML = `
            <div class="no-results">
                <i class="fa-solid fa-search"></i>
                <h3>No modules found</h3>
                <p>Try adjusting your search or filter to find what you're looking for.</p>
            </div>
        `;
    }

    /**
     * Truncate text with ellipsis
     */
    truncate(text, maxLength) {
        if (!text) return '';
        if (text.length <= maxLength) return text;
        return text.substring(0, maxLength).trim() + '...';
    }
}

// ============================================
// HOMEPAGE CONTROLLER
// ============================================

class HomePageController {
    constructor() {
        this.moduleData = [];
        this.filteredData = [];
        this.currentYear = 'all';
        this.currentQuery = '';
        this.renderer = new ModuleCardRenderer('moduleGrid');
    }

    /**
     * Initialize homepage
     */
    async init() {
        await this.loadModules();
        this.setupFilters();
        this.setupSearch();
        this.render();
        this.updateStats();
    }

    /**
     * Load module data from JSON
     */
    async loadModules() {
        try {
            const response = await fetch('data/modules.json');
            const data = await response.json();
            this.moduleData = this.flattenData(data);
            this.filteredData = [...this.moduleData];
        } catch (error) {
            console.error('Failed to load modules:', error);
            this.moduleData = [];
            this.filteredData = [];
        }
    }

    /**
     * Flatten nested JSON structure
     */
    flattenData(data) {
        const flat = [];

        for (const [yearKey, yearData] of Object.entries(data)) {
            for (const [semesterKey, semesterData] of Object.entries(yearData)) {
                for (const module of semesterData.modules || []) {
                    flat.push({
                        ...module,
                        year: yearKey,
                        yearNumber: parseInt(yearKey.replace('year', '')),
                        semester: semesterKey,
                        semesterName: semesterData.name,
                        slug: this.slugify(module.name),
                        url: `modules/${yearKey}/${this.slugify(module.name)}.html`
                    });
                }
            }
        }

        return flat;
    }

    /**
     * Create URL-friendly slug
     */
    slugify(text) {
        return text.toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-|-$/g, '');
    }

    /**
     * Setup year filter buttons
     */
    setupFilters() {
        const filterBtns = document.querySelectorAll('.filter-btn');
        
        filterBtns.forEach(btn => {
            btn.addEventListener('click', () => {
                const year = btn.dataset.year;
                
                // Update active state
                filterBtns.forEach(b => b.classList.remove('active'));
                btn.classList.add('active');
                
                // Apply filter
                this.currentYear = year;
                this.applyFilters();
            });
        });
    }

    /**
     * Setup search on homepage
     */
    setupSearch() {
        const searchInput = document.getElementById('searchInput');
        if (!searchInput) return;

        const clearBtn = document.getElementById('clearSearch');

        searchInput.addEventListener('input', () => {
            this.currentQuery = searchInput.value;
            
            // Show/hide clear button
            if (clearBtn) {
                clearBtn.style.display = this.currentQuery ? 'block' : 'none';
            }
            
            this.applyFilters();
        });

        if (clearBtn) {
            clearBtn.addEventListener('click', () => {
                searchInput.value = '';
                this.currentQuery = '';
                clearBtn.style.display = 'none';
                this.applyFilters();
                searchInput.focus();
            });
        }
    }

    /**
     * Apply all active filters
     */
    applyFilters() {
        let results = [...this.moduleData];

        // Filter by year
        if (this.currentYear !== 'all') {
            results = results.filter(m => m.year === this.currentYear);
        }

        // Filter by search query
        if (this.currentQuery && this.currentQuery.trim().length >= 2) {
            const query = this.currentQuery.toLowerCase().trim();
            results = results.filter(module => {
                return (
                    module.name.toLowerCase().includes(query) ||
                    (module.code || '').toLowerCase().includes(query) ||
                    (module.description || '').toLowerCase().includes(query) ||
                    (module.tags || []).some(tag => tag.toLowerCase().includes(query)) ||
                    (module.projects || []).some(project =>
                        (project.title || '').toLowerCase().includes(query) ||
                        (project.description || '').toLowerCase().includes(query)
                    )
                );
            });
        }

        this.filteredData = results;
        this.render();
    }

    /**
     * Render module cards
     */
    render() {
        this.renderer.render(this.filteredData);
    }

    /**
     * Update homepage stats
     */
    updateStats() {
        const totalModules = this.moduleData.length;
        const totalProjects = this.moduleData.reduce((sum, m) => {
            return sum + (m.projects ? m.projects.length : 0);
        }, 0);

        this.animateStat('statModules', totalModules);
        this.animateStat('statProjects', totalProjects);
    }

    /**
     * Animate a stat number
     */
    animateStat(elementId, target) {
        const element = document.getElementById(elementId);
        if (!element) return;

        element.textContent = target;
    }
}

// ============================================
// FEATURED PROJECTS
// ============================================

class FeaturedProjects {
    constructor(containerId = 'featuredGrid') {
        this.container = document.getElementById(containerId);
    }

    /**
     * Render featured projects
     */
    render(modules) {
        if (!this.container) return;

        // Pick featured projects (first project from random modules)
        const featured = [];
        const shuffled = [...modules].sort(() => 0.5 - Math.random());

        for (const module of shuffled) {
            if (module.projects && module.projects.length > 0 && featured.length < 6) {
                featured.push({
                    module: module,
                    project: module.projects[0]
                });
            }
        }

        this.container.innerHTML = featured.map(({ module, project }) => `
            <a href="${module.url}" class="featured-card">
                <div class="featured-card-icon">
                    <i class="fa-solid ${this.getIcon(module.icon)}"></i>
                </div>
                <div class="featured-card-content">
                    <span class="featured-module">${module.name}</span>
                    <h4>${project.title}</h4>
                    <p>${project.description || ''}</p>
                </div>
                <span class="featured-difficulty ${(project.difficulty || 'Beginner').toLowerCase()}">
                    ${project.difficulty || 'Beginner'}
                </span>
            </a>
        `).join('');
    }

    getIcon(iconType) {
        const map = {
            'programming': 'fa-code',
            'networking': 'fa-network-wired',
            'security': 'fa-shield-haltered',
            'data': 'fa-database',
            'systems': 'fa-server',
            'ai': 'fa-brain'
        };
        return map[iconType] || 'fa-book';
    }
}

// ============================================
// INITIALIZATION
// ============================================

document.addEventListener('DOMContentLoaded', async () => {
    
    // Initialize homepage if module grid exists
    if (document.getElementById('moduleGrid')) {
        const homePage = new HomePageController();
        await homePage.init();

        // Render featured projects
        if (document.getElementById('featuredGrid')) {
            const featured = new FeaturedProjects('featuredGrid');
            featured.render(homePage.moduleData);
        }
    }

    // Initialize search page if it exists
    if (document.getElementById('searchResults') || document.getElementById('searchPageInput')) {
        if (typeof searchUI !== 'undefined') {
            await searchEngine.init();
            searchUI.init();
        }
    }

    // Initialize module detail page if it exists
    if (document.querySelector('.module-hero')) {
        initModuleDetailPage();
    }
});

// ============================================
// MODULE DETAIL PAGE
// ============================================

function initModuleDetailPage() {
    // Project toggle handlers
    document.querySelectorAll('.project-header').forEach(header => {
        header.addEventListener('click', function() {
            const body = this.nextElementSibling;
            const isOpen = body.classList.contains('open');
            
            if (isOpen) {
                body.classList.remove('open');
                this.classList.remove('open');
            } else {
                body.classList.add('open');
                this.classList.add('open');
            }
        });
    });

    // Open first project by default
    const firstProject = document.querySelector('.project-header');
    if (firstProject) {
        firstProject.click();
    }
}

// ============================================
// EXPORT FOR GLOBAL USE
// ============================================

window.ModuleCardRenderer = ModuleCardRenderer;
window.HomePageController = HomePageController;
window.FeaturedProjects = FeaturedProjects;