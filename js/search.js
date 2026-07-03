/**
 * ICN Blog — Search Engine
 * Full-text search across all modules, projects, and code
 */

// ============================================
// SEARCH INDEX
// ============================================

class SearchEngine {
    constructor() {
        this.modules = [];
        this.index = {};
        this.initialized = false;
    }

    /**
     * Load module data and build search index
     */
    async init() {
        if (this.initialized) return;

        try {
            const response = await fetch('data/modules.json');
            const data = await response.json();
            this.modules = this.flattenModules(data);
            this.buildIndex();
            this.initialized = true;
        } catch (error) {
            console.error('Failed to load search index:', error);
            this.modules = [];
        }
    }

    /**
     * Flatten nested JSON into searchable array
     */
    flattenModules(data) {
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
     * Build search index for fast lookup
     */
    buildIndex() {
        this.index = {
            byTitle: {},
            byTag: {},
            byCode: {},
            byYear: {},
            all: []
        };

        this.modules.forEach(module => {
            // Index by title words
            const titleWords = module.name.toLowerCase().split(/\s+/);
            titleWords.forEach(word => {
                if (!this.index.byTitle[word]) {
                    this.index.byTitle[word] = [];
                }
                this.index.byTitle[word].push(module);
            });

            // Index by tags
            (module.tags || []).forEach(tag => {
                const normalizedTag = tag.toLowerCase();
                if (!this.index.byTag[normalizedTag]) {
                    this.index.byTag[normalizedTag] = [];
                }
                this.index.byTag[normalizedTag].push(module);
            });

            // Index by year
            const yearKey = `year${module.yearNumber}`;
            if (!this.index.byYear[yearKey]) {
                this.index.byYear[yearKey] = [];
            }
            this.index.byYear[yearKey].push(module);

            // Add to all
            this.index.all.push(module);
        });
    }

    /**
     * Search modules by query
     * Returns ranked results
     */
    search(query, options = {}) {
        if (!query || query.trim().length < 2) {
            return this.modules.slice(0, options.limit || 20);
        }

        const q = query.toLowerCase().trim();
        const results = new Map(); // Use Map to track scores

        this.modules.forEach(module => {
            let score = 0;

            // Exact title match (highest priority)
            if (module.name.toLowerCase() === q) {
                score += 100;
            }

            // Title starts with query
            if (module.name.toLowerCase().startsWith(q)) {
                score += 50;
            }

            // Title contains query
            if (module.name.toLowerCase().includes(q)) {
                score += 30;
            }

            // Title word matches
            const titleWords = module.name.toLowerCase().split(/\s+/);
            titleWords.forEach(word => {
                if (word === q) score += 25;
                if (word.startsWith(q)) score += 15;
                if (word.includes(q)) score += 10;
            });

            // Description match
            if ((module.description || '').toLowerCase().includes(q)) {
                score += 15;
            }

            // Code match
            const moduleCode = (module.code || '').toLowerCase();
            if (moduleCode === q) score += 40;
            if (moduleCode.includes(q)) score += 20;

            // Tag match
            (module.tags || []).forEach(tag => {
                if (tag === q) score += 20;
                if (tag.startsWith(q)) score += 10;
                if (tag.includes(q)) score += 5;
            });

            // Project title match
            (module.projects || []).forEach(project => {
                const projectTitle = (project.title || '').toLowerCase();
                if (projectTitle === q) score += 25;
                if (projectTitle.includes(q)) score += 15;

                // Search in project code
                if ((project.code || '').toLowerCase().includes(q)) {
                    score += 5;
                }
            });

            // Year match
            if (module.year === q || `year ${module.yearNumber}` === q) {
                score += 15;
            }

            // Only include if there's any match
            if (score > 0) {
                results.set(module, score);
            }
        });

        // Sort by score (highest first)
        const sorted = Array.from(results.entries())
            .sort((a, b) => b[1] - a[1])
            .map(entry => ({
                module: entry[0],
                score: entry[1],
                relevance: this.getRelevanceLabel(entry[1])
            }));

        return sorted.slice(0, options.limit || 50);
    }

    /**
     * Get human-readable relevance label
     */
    getRelevanceLabel(score) {
        if (score >= 80) return 'Best match';
        if (score >= 50) return 'Strong match';
        if (score >= 25) return 'Good match';
        if (score >= 10) return 'Related';
        return 'Partial match';
    }

    /**
     * Filter by year
     */
    filterByYear(results, year) {
        if (year === 'all' || !year) return results;
        return results.filter(r => r.module.year === year);
    }

    /**
     * Get suggestions for autocomplete
     */
    suggest(query, limit = 5) {
        if (!query || query.trim().length < 2) return [];

        const q = query.toLowerCase().trim();
        const suggestions = new Set();

        this.modules.forEach(module => {
            // Suggest module titles
            if (module.name.toLowerCase().startsWith(q)) {
                suggestions.add(module.name);
            }

            // Suggest tags
            (module.tags || []).forEach(tag => {
                if (tag.startsWith(q)) {
                    suggestions.add(tag);
                }
            });

            // Suggest project titles
            (module.projects || []).forEach(project => {
                if ((project.title || '').toLowerCase().startsWith(q)) {
                    suggestions.add(project.title);
                }
            });
        });

        return Array.from(suggestions).slice(0, limit);
    }

    /**
     * Get total module count
     */
    getModuleCount() {
        return this.modules.length;
    }

    /**
     * Get total project count
     */
    getProjectCount() {
        return this.modules.reduce((total, m) => {
            return total + (m.projects ? m.projects.length : 0);
        }, 0);
    }

    /**
     * Get all unique tags
     */
    getAllTags() {
        const tags = new Set();
        this.modules.forEach(m => {
            (m.tags || []).forEach(tag => tags.add(tag));
        });
        return Array.from(tags).sort();
    }
}

// ============================================
// SEARCH UI
// ============================================

class SearchUI {
    constructor(engine) {
        this.engine = engine;
        this.resultsContainer = null;
        this.input = null;
        this.suggestionsContainer = null;
        this.debounceTimer = null;
    }

    /**
     * Initialize search UI elements
     */
    init() {
        this.resultsContainer = document.getElementById('searchResults');
        this.input = document.getElementById('searchPageInput') || 
                     document.getElementById('searchInput');
        this.suggestionsContainer = document.getElementById('searchSuggestions');

        if (this.input) {
            this.input.addEventListener('input', () => this.handleInput());
            this.input.addEventListener('focus', () => this.handleInput());
        }

        // Check for query parameter in URL
        const urlParams = new URLSearchParams(window.location.search);
        const query = urlParams.get('q');
        if (query && this.input) {
            this.input.value = query;
            this.performSearch(query);
        }
    }

    /**
     * Handle input changes with debounce
     */
    handleInput() {
        clearTimeout(this.debounceTimer);
        const query = this.input.value.trim();

        if (query.length >= 2) {
            this.debounceTimer = setTimeout(() => {
                this.showSuggestions(query);
            }, 200);
        } else {
            this.hideSuggestions();
        }
    }

    /**
     * Show autocomplete suggestions
     */
    showSuggestions(query) {
        const suggestions = this.engine.suggest(query, 5);
        
        if (suggestions.length === 0) {
            this.hideSuggestions();
            return;
        }

        if (!this.suggestionsContainer) {
            this.suggestionsContainer = document.createElement('div');
            this.suggestionsContainer.id = 'searchSuggestions';
            this.suggestionsContainer.className = 'search-suggestions';
            this.input.parentNode.appendChild(this.suggestionsContainer);
        }

        this.suggestionsContainer.innerHTML = suggestions.map(s => `
            <div class="suggestion-item" role="option" tabindex="0">
                <i class="fa-solid fa-magnifying-glass"></i>
                <span>${this.highlightMatch(s, query)}</span>
            </div>
        `).join('');

        this.suggestionsContainer.style.display = 'block';

        // Click handlers
        this.suggestionsContainer.querySelectorAll('.suggestion-item').forEach(item => {
            item.addEventListener('click', () => {
                this.input.value = item.textContent.trim();
                this.performSearch(this.input.value);
                this.hideSuggestions();
            });
        });
    }

    /**
     * Hide suggestions dropdown
     */
    hideSuggestions() {
        if (this.suggestionsContainer) {
            this.suggestionsContainer.style.display = 'none';
        }
    }

    /**
     * Highlight matching text
     */
    highlightMatch(text, query) {
        const regex = new RegExp(`(${query.replace(/[.*+?^${}()|[\]\\]/g, '\\$&')})`, 'gi');
        return text.replace(regex, '<mark>$1</mark>');
    }

    /**
     * Perform full search and render results
     */
    performSearch(query) {
        if (!this.resultsContainer) return;

        if (!query || query.trim().length < 2) {
            this.showEmptyState();
            return;
        }

        const results = this.engine.search(query);

        if (results.length === 0) {
            this.showNoResults(query);
            return;
        }

        this.renderResults(results, query);
    }

    /**
     * Render search results
     */
    renderResults(results, query) {
        // Group by year
        const grouped = {};
        results.forEach(({ module, score, relevance }) => {
            const year = module.year;
            if (!grouped[year]) grouped[year] = [];
            grouped[year].push({ module, score, relevance });
        });

        let html = `
            <div class="search-summary">
                <p>Found <strong>${results.length}</strong> result${results.length !== 1 ? 's' : ''} 
                for "<strong>${this.escapeHtml(query)}</strong>"</p>
            </div>
        `;

        for (const [year, items] of Object.entries(grouped)) {
            const yearLabel = year.replace('year', 'Year ');
            
            html += `
                <div class="search-group">
                    <h3 class="search-group-title">${yearLabel}</h3>
                    ${items.map(({ module, score, relevance }) => this.renderResultCard(module, relevance, query)).join('')}
                </div>
            `;
        }

        this.resultsContainer.innerHTML = html;
        this.resultsContainer.style.display = 'block';

        // Update URL without reloading
        if (history.pushState) {
            const newUrl = `${window.location.pathname}?q=${encodeURIComponent(query)}`;
            history.pushState({ path: newUrl }, '', newUrl);
        }
    }

    /**
     * Render a single result card
     */
    renderResultCard(module, relevance, query) {
        const iconMap = {
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

        const icon = iconMap[module.icon] || 'fa-book';
        const projectCount = module.projects ? module.projects.length : 0;
        const highlightedName = this.highlightMatch(module.name, query);
        const highlightedDesc = this.highlightMatch(
            module.description ? module.description.substring(0, 150) : '', 
            query
        );

        return `
            <a href="${module.url}" class="search-result-card">
                <div class="result-icon">
                    <i class="fa-solid ${icon}"></i>
                </div>
                <div class="result-content">
                    <div class="result-header">
                        <h4>${highlightedName}</h4>
                        <span class="result-code">${module.code || ''}</span>
                        <span class="result-relevance ${relevance.toLowerCase().replace(/\s+/g, '-')}">${relevance}</span>
                    </div>
                    <p class="result-description">${highlightedDesc}${module.description && module.description.length > 150 ? '...' : ''}</p>
                    <div class="result-meta">
                        <span><i class="fa-solid fa-calendar"></i> ${module.semesterName}</span>
                        <span><i class="fa-solid fa-code"></i> ${projectCount} project${projectCount !== 1 ? 's' : ''}</span>
                        <span class="result-tags">
                            ${(module.tags || []).slice(0, 3).map(tag => 
                                `<span class="result-tag">${this.highlightMatch(tag, query)}</span>`
                            ).join('')}
                        </span>
                    </div>
                </div>
                <div class="result-arrow">
                    <i class="fa-solid fa-chevron-right"></i>
                </div>
            </a>
        `;
    }

    /**
     * Show empty state
     */
    showEmptyState() {
        if (!this.resultsContainer) return;
        
        this.resultsContainer.innerHTML = `
            <div class="search-empty">
                <i class="fa-solid fa-search"></i>
                <h3>Search Modules</h3>
                <p>Type at least 2 characters to search across all ${this.engine.getModuleCount()} modules and ${this.engine.getProjectCount()} projects.</p>
                <div class="popular-tags">
                    <p>Popular topics:</p>
                    ${this.engine.getAllTags().slice(0, 8).map(tag => 
                        `<span class="popular-tag" onclick="document.getElementById('searchPageInput').value='${tag}'; document.getElementById('searchPageInput').dispatchEvent(new Event('input'));">${tag}</span>`
                    ).join('')}
                </div>
            </div>
        `;
    }

    /**
     * Show no results state
     */
    showNoResults(query) {
        if (!this.resultsContainer) return;

        this.resultsContainer.innerHTML = `
            <div class="search-empty">
                <i class="fa-solid fa-face-frown"></i>
                <h3>No results found</h3>
                <p>We couldn't find anything matching "<strong>${this.escapeHtml(query)}</strong>"</p>
                <p>Try:</p>
                <ul>
                    <li>Checking your spelling</li>
                    <li>Using fewer words</li>
                    <li>Searching for a specific technology (e.g., "python", "scapy")</li>
                    <li>Browsing by year using the filters above</li>
                </ul>
            </div>
        `;
    }

    /**
     * Escape HTML to prevent XSS
     */
    escapeHtml(text) {
        const div = document.createElement('div');
        div.textContent = text;
        return div.innerHTML;
    }
}

// ============================================
// INITIALIZATION
// ============================================

const searchEngine = new SearchEngine();
const searchUI = new SearchUI(searchEngine);

document.addEventListener('DOMContentLoaded', async () => {
    await searchEngine.init();
    searchUI.init();

    // Expose for global use
    window.searchEngine = searchEngine;
    window.searchUI = searchUI;
});