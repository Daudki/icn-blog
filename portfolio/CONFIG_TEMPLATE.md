/**
 * GitHub Portfolio Integration - Configuration Template
 * 
 * Copy and paste configuration options into js/github-integration.js
 * Uncomment the options you want to use
 */

// ============================================
// BASIC CONFIGURATION
// ============================================

// 1️⃣ SET YOUR GITHUB USERNAME (REQUIRED)
// const GITHUB_USERNAME = 'your-github-username';

// ============================================
// CONTENT CONFIGURATION
// ============================================

// 2️⃣ SHOW ONLY YOUR BEST REPOSITORIES
// CONFIG.maxRepos = 10;  // Default: 100 (max: 100)

// 3️⃣ INCLUDE FORKED REPOSITORIES
// CONFIG.includeForked = true;  // Default: false

// 4️⃣ HIDE STARS AND FORKS COUNTS
// CONFIG.showStats = false;  // Default: true

// ============================================
// SORTING OPTIONS
// ============================================

// 5️⃣ SORT BY MOST POPULAR (STARS)
// CONFIG.sortBy = 'stars';

// 6️⃣ SORT BY MOST FORKED
// CONFIG.sortBy = 'forks';

// 7️⃣ SORT ALPHABETICALLY BY NAME
// CONFIG.sortBy = 'name';

// 8️⃣ DEFAULT: SORT BY RECENTLY UPDATED
// CONFIG.sortBy = 'updated';

// ============================================
// AUTO-REFRESH CONFIGURATION
// ============================================

// 9️⃣ ENABLE AUTO-REFRESH (Every 5 minutes)
// setupAutoRefresh();

// 🔟 CUSTOM AUTO-REFRESH INTERVAL
// setupAutoRefresh(10 * 60 * 1000);  // Every 10 minutes
// setupAutoRefresh(1 * 60 * 1000);   // Every 1 minute
// setupAutoRefresh(30 * 60 * 1000);  // Every 30 minutes

// ============================================
// DEBUGGING & DEVELOPMENT
// ============================================

// 1️⃣1️⃣ ENABLE DEBUG MODE (See console logs)
// CONFIG.debug = true;  // Default: false

// 1️⃣2️⃣ LISTEN TO REPOS LOADED EVENT
// window.addEventListener('github-repos-loaded', (event) => {
//     console.log('Repos loaded:', event.detail);
//     console.log('Total repos:', event.detail.count);
//     console.log('Repos array:', event.detail.repos);
// });

// ============================================
// LANGUAGE COLORS
// ============================================

// 1️⃣3️⃣ ADD CUSTOM LANGUAGE COLORS
// In getLanguageColor() function, add:
// const languageColors = {
//     'YourLanguage': '#FF5733',
//     'AnotherLang': '#33FF57',
//     // ... existing colors ...
// };

// ============================================
// ADVANCED: MODIFY CARD DISPLAY
// ============================================

// 1️⃣4️⃣ LIMIT DESCRIPTION LENGTH
// In createProjectCard() function, change:
// description.substring(0, 100)  →  description.substring(0, 200)

// 1️⃣5️⃣ SHOW MORE TOPICS
// In createProjectCard() function, change:
// topics.slice(0, 3)  →  topics.slice(0, 5)

// ============================================
// COMPLETE EXAMPLE CONFIGURATION
// ============================================

/*
// At the top of js/github-integration.js, after CONFIG declaration:

const GITHUB_USERNAME = 'my-github-username';

// In CONFIG object:
const CONFIG = {
    includeForked: false,        // Exclude forked repos
    sortBy: 'stars',             // Show most popular first
    maxRepos: 50,                // Show 50 most popular
    showStats: true,             // Show stars/forks
    debug: true                  // Enable debug logging
};

// At the bottom of the file:
setupAutoRefresh(5 * 60 * 1000);  // Refresh every 5 minutes

// Listen for when repos are loaded
window.addEventListener('github-repos-loaded', (event) => {
    console.log(`Loaded ${event.detail.count} repositories`);
});
*/

// ============================================
// CACHING INFORMATION
// ============================================

// Cache Details:
// - Key: github_repos_{GITHUB_USERNAME}
// - Duration: 30 minutes
// - Stored in: localStorage
// - Clear cache: localStorage.removeItem('github_repos_YOUR_USERNAME')

// To clear cache programmatically:
// localStorage.removeItem(`github_repos_${GITHUB_USERNAME}`);

// ============================================
// API RATE LIMITS
// ============================================

// GitHub API Rate Limits:
// - Unauthenticated: 60 requests/hour
// - Authenticated: 5,000 requests/hour

// Your usage (with examples):
// - Without auto-refresh: ~1 request per page load
// - With 5-min auto-refresh: 288 requests/day
// - With 1-min auto-refresh: 1,440 requests/day (within limits)

// ============================================
// RESPONSIVE BREAKPOINTS
// ============================================

// Portfolio automatically adjusts:
// - Desktop (>992px): 3-column grid
// - Tablet (768px-992px): 2-column grid
// - Mobile (<768px): 1-column grid

// ============================================
// BROWSER SUPPORT
// ============================================

// Works on:
// - Chrome/Edge 90+
// - Firefox 88+
// - Safari 14+
// - All modern browsers with ES6 support

// ============================================
// COMMON SETUP PATTERNS
// ============================================

// Pattern 1: Show only personal projects, sorted by popularity
// const GITHUB_USERNAME = 'your-username';
// CONFIG.includeForked = false;
// CONFIG.sortBy = 'stars';
// CONFIG.maxRepos = 25;
// setupAutoRefresh();

// Pattern 2: Include everything, recently updated
// const GITHUB_USERNAME = 'your-username';
// CONFIG.includeForked = true;
// CONFIG.sortBy = 'updated';
// CONFIG.maxRepos = 100;

// Pattern 3: Debug setup for development
// const GITHUB_USERNAME = 'your-username';
// CONFIG.debug = true;
// setupAutoRefresh(1 * 60 * 1000); // Refresh every minute for testing

// ============================================
// RESET TO DEFAULTS
// ============================================

// To reset to original configuration:
// 1. Remove all CONFIG customizations
// 2. Comment out setupAutoRefresh()
// 3. Reload portfolio
// 4. Clear cache: localStorage.removeItem('github_repos_YOUR_USERNAME')
