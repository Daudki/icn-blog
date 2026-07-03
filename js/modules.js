/**
 * ICN Blog — Module Management
 * Handles loading module data, rendering cards, and filtering
 */

class ModuleManager {
    constructor() {
        this.modules = [];
        this.filteredModules = [];
        this.currentYear = 'all';
    }

    /**
     * Load module data from JSON
     */
    async loadModules() {
        try {
            const response = await fetch('data/modules.json');
            const data = await response.json();
            this.modules = this.flattenModules(data);
            this.filteredModules = [...this.modules];
            return this.modules;
        } catch (error) {
            console.error('Failed to load modules:', error);
            return [];
        }
    }

    /**
     * Flatten nested JSON structure into array of modules
     */
    flattenModules(data) {
        const flat = [];
        
        for (const [yearKey, yearData] of Object.entries(data)) {
            for (const [semesterKey, semesterData] of Object.entries(yearData)) {
                for (const module of semesterData.modules) {
                    flat.push({
                        ...module,
                        year: yearKey,
                        yearNumber: parseInt(yearKey.replace('year', '')),
                        semester: semesterKey,
                        semesterName: semesterData.name,
                        slug: this.generateSlug(module.name),
                        url: `modules/${yearKey}/${this.generateSlug(module.name)}.html`
                    });
                }
            }
        }
        
        return flat;
    }

    /**
     * Generate URL-friendly slug from module name
     */
    generateSlug(name) {
        return name.toLowerCase()
            .replace(/[^a-z0-9]+/g, '-')
            .replace(/^-|-$/g, '');
    }

    /**
     * Filter modules by year
     */
    filterByYear(year) {
        this.currentYear = year;
        
        if (year === 'all') {
            this.filteredModules = [...this.modules];
        } else {
            this.filteredModules = this.modules.filter(m => m.year === year);
        }
        
        return this.filteredModules;
    }

    /**
     * Search modules by query
     */
    search(query) {
        if (!query || query.trim() === '') {
            this.filteredModules = this.filterByYear(this.currentYear);
            return this.filteredModules;
        }
        
        const lowerQuery = query.toLowerCase().trim();
        
        this.filteredModules = this.modules.filter(module => {
            return (
                module.name.toLowerCase().includes(lowerQuery) ||
                module.code.toLowerCase().includes(lowerQuery) ||
                module.description.toLowerCase().includes(lowerQuery) ||
                (module.tags && module.tags.some(tag => tag.includes(lowerQuery)))
            );
        });
        
        return this.filteredModules;
    }

    /**
     * Get icon class based on module icon type
     */
    getIconClass(iconType) {
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
            'hacking': 'fa-user-secret',
            'default': 'fa-book'
        };
        return iconMap[iconType] || iconMap['default'];
    }

    /**
     * Get color class for module card icon
     */
    getIconColorClass(iconType) {
        const validTypes = ['networking', 'security', 'programming', 'data', 'systems'];
        return validTypes.includes(iconType) ? iconType : 'networking';
    }

    /**
     * Render module cards to the grid
     */
    renderCards(containerId = 'moduleGrid') {
        const container = document.getElementById(containerId);
        if (!container) return;
        
        if (this.filteredModules.length === 0) {
            container.innerHTML = `
                <div class="no-results">
                    <i class="fa-solid fa-search"></i>
                    <h3>No modules found</h3>
                    <p>Try a different search term or filter.</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = this.filteredModules.map(module => this.createCardHTML(module)).join('');
        
        // Add click handlers
        container.querySelectorAll('.module-card').forEach(card => {
            card.addEventListener('click', () => {
                window.location.href = card.dataset.url;
            });
        });
    }

    /**
     * Create HTML for a single module card
     */
    createCardHTML(module) {
        const iconClass = this.getIconClass(module.icon);
        const colorClass = this.getIconColorClass(module.icon);
        const projectCount = module.projects ? module.projects.length : 0;
        
        return `
            <div class="module-card" data-url="${module.url}">
                <div class="module-card-icon ${colorClass}">
                    <i class="fa-solid ${iconClass}"></i>
                </div>
                <span class="module-card-code">${module.code}</span>
                <h3>${module.name}</h3>
                <p>${module.description}</p>
                <div class="module-card-meta">
                    <span><i class="fa-solid fa-calendar"></i> Year ${module.yearNumber}</span>
                    <span><i class="fa-solid fa-clock"></i> ${module.semesterName}</span>
                </div>
                <div class="module-card-projects">
                    <i class="fa-solid fa-code"></i> ${projectCount} Project${projectCount !== 1 ? 's' : ''}
                </div>
            </div>
        `;
    }

    /**
     * Get total module count
     */
    getTotalCount() {
        return this.modules.length;
    }

    /**
     * Get total project count
     */
    getTotalProjectCount() {
        return this.modules.reduce((total, module) => {
            return total + (module.projects ? module.projects.length : 0);
        }, 0);
    }
}

// Global instance
const moduleManager = new ModuleManager();