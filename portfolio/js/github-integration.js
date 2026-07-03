/**
 * GitHub Portfolio Integration
 * Fetches and displays repositories from GitHub in real-time
 * 
 * Configuration:
 * - Update GITHUB_USERNAME with your GitHub handle
 * - Uncomment setupAutoRefresh() at the bottom to enable auto-refresh
 */

const GITHUB_USERNAME = 'Daudki'; // ⚙️ CHANGE THIS TO YOUR GITHUB USERNAME
const GITHUB_API_URL = `https://api.github.com/users/${GITHUB_USERNAME}/repos`;
const CACHE_KEY = `github_repos_${GITHUB_USERNAME}`;
const CACHE_DURATION = 30 * 60 * 1000; // 30 minutes cache

// Configuration flags
const CONFIG = {
    includeForked: false,        // Set to true to include forked repos
    sortBy: 'updated',           // Options: 'updated', 'stars', 'forks', 'name'
    maxRepos: 100,               // Maximum repos to display (1-100)
    showStats: true,             // Show stars and forks count
    debug: false                 // Enable console logging for debugging
};

/**
 * Log debug information (only if debug mode is enabled)
 */
function debugLog(message, data = null) {
    if (CONFIG.debug) {
        console.log(`[GitHub Integration] ${message}`, data || '');
    }
}

/**
 * Get cached repositories
 */
function getCachedRepos() {
    const cached = localStorage.getItem(CACHE_KEY);
    if (!cached) return null;
    
    const { data, timestamp } = JSON.parse(cached);
    if (Date.now() - timestamp > CACHE_DURATION) {
        localStorage.removeItem(CACHE_KEY);
        return null;
    }
    
    debugLog('Loaded from cache');
    return data;
}

/**
 * Cache repositories locally
 */
function cacheRepos(repos) {
    try {
        localStorage.setItem(CACHE_KEY, JSON.stringify({
            data: repos,
            timestamp: Date.now()
        }));
        debugLog('Cached repositories');
    } catch (e) {
        debugLog('Failed to cache repositories', e);
    }
}

/**
 * Fetch repositories from GitHub API
 */
async function fetchGitHubRepos() {
    try {
        debugLog(`Fetching repositories for ${GITHUB_USERNAME}...`);
        
        const response = await fetch(
            `${GITHUB_API_URL}?sort=${CONFIG.sortBy}&per_page=${CONFIG.maxRepos}`,
            {
                headers: {
                    'Accept': 'application/vnd.github.v3+json'
                }
            }
        );
        
        if (!response.ok) {
            throw new Error(`GitHub API error: ${response.status} ${response.statusText}`);
        }
        
        const repos = await response.json();
        debugLog(`Found ${repos.length} total repositories`);
        
        // Filter repositories
        let filtered = repos;
        
        if (!CONFIG.includeForked) {
            filtered = repos.filter(repo => !repo.fork);
            debugLog(`Filtered to ${filtered.length} repositories (excluded forks)`);
        }
        
        // Sort by updated date if using other sort method
        if (CONFIG.sortBy !== 'updated') {
            filtered.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
        }
        
        // Cache the results
        cacheRepos(filtered);
        
        return filtered;
    } catch (error) {
        console.error('Error fetching GitHub repos:', error);
        debugLog('API Error', error.message);
        
        // Try to use cached data if API fails
        const cached = getCachedRepos();
        if (cached) {
            console.warn('Using cached repository data');
            return cached;
        }
        
        return [];
    }
}

/**
 * Get language color for project tags
 */
function getLanguageColor(language) {
    const languageColors = {
        // Popular languages
        'JavaScript': '#f1e05a',
        'TypeScript': '#3178c6',
        'Python': '#3572A5',
        'Java': '#b07219',
        'C++': '#f34b7d',
        'C#': '#239120',
        'PHP': '#777bb4',
        'Go': '#00ADD8',
        'Rust': '#dea584',
        'Ruby': '#cc342d',
        // Frontend
        'HTML': '#e34c26',
        'CSS': '#563d7c',
        'Vue': '#41b883',
        'React': '#61dafb',
        // Backend
        'Node.js': '#68a063',
        'Express': '#90c53f',
        'Django': '#092E20',
        'Flask': '#000000',
        // Other
        'Shell': '#89e051',
        'Dockerfile': '#384d54',
        'YAML': '#cb171e',
        'JSON': '#000000',
    };
    return languageColors[language] || '#858585';
}

function createLoadingSkeleton(count = 3) {
    return Array.from({ length: count }).map(() => `
        <div class="project-card skeleton-card" aria-hidden="true">
            <div class="project-image skeleton-block"></div>
            <div class="project-content">
                <div class="skeleton-line skeleton-title"></div>
                <div class="skeleton-line skeleton-text"></div>
                <div class="skeleton-line skeleton-text short"></div>
                <div class="project-tags">
                    <span class="project-tag skeleton-tag"></span>
                    <span class="project-tag skeleton-tag short"></span>
                </div>
                <div class="project-actions">
                    <span class="btn btn-secondary skeleton-button"></span>
                    <span class="btn btn-secondary skeleton-button"></span>
                </div>
            </div>
        </div>
    `).join('');
}

/**
 * Create a project card HTML element
 */
function createProjectCard(repo, index) {
    const description = repo.description || 'No description available';
    const language = repo.language || 'Code';
    const stars = repo.stargazers_count || 0;
    const forks = repo.forks_count || 0;
    const topics = repo.topics || [];
    
    // Generate a consistent placeholder image based on repo name
    const placeholderImages = {
        'JavaScript': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8amF2YXNjcmlwdHxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=1200&q=80',
        'Python': 'https://images.unsplash.com/photo-1526374965328-7f5ae4e8a0c5?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8Mnx8cHl0aG9ufGVufDB8fDB8fHw%3D&auto=format&fit=crop&w=1200&q=80',
        'HTML': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'CSS': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&auto=format&fit=crop&w=1200&q=80',
        'default': 'https://images.unsplash.com/photo-1517694712202-14dd9538aa97?ixlib=rb-4.0.3&ixid=M3wxMjA3fDB8MHxzZWFyY2h8MXx8Y29kZXxlbnwwfHwwfHw%3D&auto=format&fit=crop&w=1200&q=80'
    };
    
    const imageUrl = placeholderImages[language] || placeholderImages['default'];
    
    // Build tags HTML with animation delay
    let tagsHTML = `<span class="project-tag" style="background: ${getLanguageColor(language)}; color: white; animation-delay: ${index * 50}ms;">`;
    tagsHTML += `<i class="fas fa-code"></i> ${language}</span>`;
    
    topics.slice(0, 3).forEach((topic, i) => {
        tagsHTML += `<span class="project-tag" style="animation-delay: ${(index + i + 1) * 50}ms;">${topic}</span>`;
    });
    
    // Add repository stats
    if (CONFIG.showStats) {
        if (stars > 0) {
            tagsHTML += `<span class="project-tag" style="animation-delay: ${(index + 4) * 50}ms;"><i class="fas fa-star"></i> ${stars}</span>`;
        }
        if (forks > 0) {
            tagsHTML += `<span class="project-tag" style="animation-delay: ${(index + 5) * 50}ms;"><i class="fas fa-code-branch"></i> ${forks}</span>`;
        }
    }
    
    // Format dates
    const updatedDate = new Date(repo.updated_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
    
    const createdDate = new Date(repo.created_at).toLocaleDateString('en-US', {
        year: 'numeric',
        month: 'short',
        day: 'numeric'
    });
    
    const card = document.createElement('div');
    card.className = 'project-card reveal-on-scroll';
    card.style.animationDelay = `${index * 100}ms`;
    
    const repoUrl = repo.html_url;
    const cloneUrl = repo.clone_url;
    
    card.innerHTML = `
        <div class="project-image">
            <img src="${imageUrl}" 
                 alt="${repo.name}" 
                 loading="lazy"
                 onerror="this.src='https://via.placeholder.com/400x300?text=${encodeURIComponent(repo.name)}'">
        </div>
        <div class="project-content">
            <h3 class="project-title">${repo.name}</h3>
            <p class="project-desc">${description.substring(0, 120)}${description.length > 120 ? '...' : ''}</p>
            
            <div class="project-meta">
                <span class="project-date">
                    <i class="fas fa-calendar"></i> Updated: ${updatedDate}
                </span>
            </div>
            
            <div class="project-tags">
                ${tagsHTML}
            </div>
            
            <div class="project-actions">
                <a href="${repoUrl}" target="_blank" rel="noreferrer" class="btn btn-primary" title="View repository on GitHub">
                    <i class="fas fa-external-link-alt"></i> Repo
                </a>
                <a href="${cloneUrl}" target="_blank" rel="noreferrer" class="btn btn-secondary" title="Clone command: git clone ${cloneUrl}">
                    <i class="fab fa-github"></i> Clone
                </a>
            </div>
        </div>
    `;
    
    return card;
}

/**
 * Initialize GitHub projects display
 */
async function initializeGitHubProjects() {
    const projectsContainer = document.querySelector('.projects-container');
    
    if (!projectsContainer) {
        console.error('Projects container not found - ensure ".projects-container" exists in HTML');
        return;
    }
    
    debugLog('Initializing GitHub projects...');
    projectsContainer.setAttribute('aria-busy', 'true');
    projectsContainer.classList.add('loading');
    projectsContainer.innerHTML = createLoadingSkeleton(3);
    
    try {
        // Fetch repositories
        const repos = await fetchGitHubRepos();
        debugLog(`Retrieved ${repos.length} repositories`);
        
        if (repos.length === 0) {
            projectsContainer.innerHTML = `
                <div class="empty-state" role="status">
                    <i class="fas fa-inbox" aria-hidden="true"></i>
                    <p>No repositories found.</p>
                    <p>Create some repositories on 
                        <a href="https://github.com/${GITHUB_USERNAME}" target="_blank" rel="noreferrer">GitHub</a> to see them here.
                    </p>
                </div>
            `;
            projectsContainer.setAttribute('aria-busy', 'false');
            projectsContainer.classList.remove('loading');
            return;
        }
        
        // Clear container
        projectsContainer.innerHTML = '';
        
        // Add repository cards with staggered animation
        repos.forEach((repo, index) => {
            const card = createProjectCard(repo, index);
            projectsContainer.appendChild(card);
        });
        
        projectsContainer.setAttribute('aria-busy', 'false');
        projectsContainer.classList.remove('loading');
        
        debugLog(`Rendered ${repos.length} project cards`);
        
        // Dispatch custom event for other scripts to hook into
        window.dispatchEvent(new CustomEvent('github-repos-loaded', { detail: { repos, count: repos.length } }));
        
    } catch (error) {
        console.error('Failed to initialize GitHub projects:', error);
        debugLog('Initialization Error', error);
        
        projectsContainer.innerHTML = `
            <div class="empty-state" role="alert">
                <i class="fas fa-exclamation-triangle" aria-hidden="true"></i>
                <p>Failed to load repositories.</p>
                <p>Check your internet connection and verify the GitHub username is correct.</p>
                <button type="button" class="btn btn-primary" onclick="location.reload()">
                    <i class="fas fa-redo" aria-hidden="true"></i>
                    Retry
                </button>
            </div>
        `;
        projectsContainer.setAttribute('aria-busy', 'false');
        projectsContainer.classList.remove('loading');
    }
}

/**
 * Set up auto-refresh (optional - updates every 5 minutes by default)
 * @param {number} interval - Time in milliseconds between refreshes (default: 5 minutes)
 */
function setupAutoRefresh(interval = 5 * 60 * 1000) {
    debugLog(`Auto-refresh enabled with ${interval / 1000 / 60} minute interval`);
    
    setInterval(() => {
        debugLog('Auto-refreshing repositories...');
        initializeGitHubProjects();
    }, interval);
    
    // Also refresh on page visibility change (when user returns to tab)
    document.addEventListener('visibilitychange', () => {
        if (!document.hidden) {
            debugLog('Page became visible, refreshing repositories...');
            initializeGitHubProjects();
        }
    });
}

// ============================================
// INITIALIZATION
// ============================================

// Initialize on DOM ready
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', initializeGitHubProjects);
} else {
    initializeGitHubProjects();
}

// ============================================
// CONFIGURATION OPTIONS
// ============================================
// 
// 1. Update your GitHub username at the top of this file
// 2. Uncomment the line below to enable auto-refresh
// 3. Customize CONFIG object above to your preferences
//

// OPTION 1: Enable auto-refresh with default 5-minute interval
// setupAutoRefresh();

// OPTION 2: Enable auto-refresh with custom interval (10 minutes)
// setupAutoRefresh(10 * 60 * 1000);

// OPTION 3: Enable debug mode
// CONFIG.debug = true;

// OPTION 4: Include forked repositories
// CONFIG.includeForked = true;

// OPTION 5: Change sorting method
// CONFIG.sortBy = 'stars'; // Options: 'updated', 'stars', 'forks', 'name'

// ============================================
// API REFERENCE
// ============================================
//
// Public Functions:
//   - initializeGitHubProjects()  → Load and display repositories
//   - fetchGitHubRepos()          → Fetch repositories from GitHub API
//   - setupAutoRefresh(interval)  → Enable automatic refresh
//
// Events Dispatched:
//   - 'github-repos-loaded'       → Fired when repos are successfully loaded
//                                   Use: window.addEventListener('github-repos-loaded', (e) => { console.log(e.detail); })
//
// Local Storage:
//   - Cache key: github_repos_${GITHUB_USERNAME}
//   - Cache duration: 30 minutes
//
// ============================================
