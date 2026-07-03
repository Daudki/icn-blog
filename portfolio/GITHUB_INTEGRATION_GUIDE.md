# GitHub Portfolio Integration - Setup & Configuration Guide

## Overview
Your portfolio now automatically displays all your GitHub repositories in real-time! Whenever you add a new repository to GitHub, it will automatically appear on your portfolio.

## Features
✅ **Real-Time Updates** - Fetches repositories from GitHub API  
✅ **Auto-Refresh** - Optional automatic refresh every 5 minutes  
✅ **Smart Filtering** - Excludes forked repositories  
✅ **Rich Metadata** - Displays language, stars, forks, topics, and last updated date  
✅ **Color-Coded Tags** - Language tags with appropriate colors  
✅ **Responsive Design** - Works perfectly on desktop, tablet, and mobile  
✅ **Error Handling** - Graceful fallbacks if GitHub API is unavailable  

## Quick Start

### 1. **Update Your GitHub Username**
Open `js/github-integration.js` and update this line with your GitHub username:
```javascript
const GITHUB_USERNAME = 'kisulodaud'; // Change this to your GitHub username
```

### 2. **Enable Auto-Refresh (Optional)**
If you want your portfolio to automatically refresh and fetch new repos every 5 minutes, uncomment this line at the bottom of `js/github-integration.js`:
```javascript
// setupAutoRefresh(); // Uncomment to enable auto-refresh
```

To customize the refresh interval (default is 5 minutes = 300000 milliseconds):
```javascript
setupAutoRefresh(10 * 60 * 1000); // Refresh every 10 minutes
```

### 3. **Done!**
That's it! Your portfolio will now display all your GitHub repositories automatically.

## How It Works

### Data Flow
1. **GitHub API Fetch** → Gets all your public repositories
2. **Filtering** → Removes forked repos, sorts by last updated
3. **Card Generation** → Creates beautiful project cards with metadata
4. **Real-Time Display** → Shows all repos on your portfolio

### What Information Is Displayed
- **Repository Name** - Title of your project
- **Description** - From the repo description (first 100 characters)
- **Primary Language** - Color-coded tag showing main language
- **Topics** - Up to 3 tags/topics from the repo
- **Stars** - Number of GitHub stars
- **Forks** - Number of times the repo has been forked
- **Last Updated** - When the repository was last updated
- **Repository Links** - Direct links to GitHub repo

## Customization

### Limit Number of Repositories Displayed
Edit `js/github-integration.js` in the `fetchGitHubRepos()` function:
```javascript
// Change per_page parameter (default: 100, max: 100)
const response = await fetch(`${GITHUB_API_URL}?sort=updated&per_page=50`);
```

### Include Forked Repositories
In `js/github-integration.js`, modify the filter:
```javascript
// Remove the .filter(repo => !repo.fork) condition to include forked repos
const filteredRepos = repos.sort((a, b) => new Date(b.updated_at) - new Date(a.updated_at));
```

### Add More Language Colors
Edit the `getLanguageColor()` function in `js/github-integration.js`:
```javascript
const languageColors = {
    'YourLanguage': '#yourcolor',
    // Add more languages here
};
```

### Change Sorting Method
By default, repositories are sorted by last updated date. Change in the API URL:
```javascript
// sort=updated (default) - sorted by last updated
// sort=stars - sorted by stars (most popular first)
// sort=forks - sorted by forks
// sort=help - sort by help wanted issues
const response = await fetch(`${GITHUB_API_URL}?sort=stars&per_page=100`);
```

## Files Modified/Created

### New Files
- `js/github-integration.js` - Main GitHub integration script

### Modified Files
- `index.html` - Updated projects section to use dynamic loading
- `css/style.css` - Added styling for project metadata

## Browser Compatibility
- ✅ Chrome/Edge 90+
- ✅ Firefox 88+
- ✅ Safari 14+
- ✅ All modern browsers with ES6 support

## API Rate Limiting
GitHub's API has rate limits:
- **Unauthenticated** - 60 requests per hour
- **Authenticated** - 5,000 requests per hour

Since the script fetches once per page load, you'll have plenty of room. If you enable auto-refresh every 5 minutes, that's 288 requests per day, well within limits.

## Troubleshooting

### Repositories Not Showing
1. Check browser console (F12 → Console) for error messages
2. Verify your GitHub username is correct in `js/github-integration.js`
3. Ensure repositories are public (private repos won't show)
4. Check GitHub API status at https://www.githubstatus.com

### Loading State Persists
- Check internet connection
- Verify GitHub API is accessible
- Look for CORS errors in browser console
- GitHub API might be temporarily unavailable

### Wrong Language Colors
Some languages might not be in the predefined colors list. Add them to `getLanguageColor()` function for consistent styling.

## Advanced Features

### Webhook Integration (Coming Soon)
For true real-time updates without page refresh, you could set up a GitHub webhook that notifies your server of new repositories.

### GitHub API Authentication
For higher rate limits, you can use a GitHub Personal Access Token:
```javascript
const response = await fetch(
    `${GITHUB_API_URL}?sort=updated&per_page=100`,
    {
        headers: {
            'Authorization': 'token YOUR_GITHUB_TOKEN_HERE'
        }
    }
);
```

## Support & Issues

If you encounter any issues:
1. Check the browser console for error messages
2. Verify all files are in the correct directories
3. Clear browser cache and refresh
4. Try in a different browser

## Tips for Best Results

1. **Write Good Descriptions** - Keep repo descriptions concise but descriptive
2. **Add Topics** - Use GitHub topics to categorize your projects
3. **Star Your Best Work** - Popular repos will show their star count
4. **Keep READMEs Updated** - While descriptions show, keep READMEs detailed
5. **Regular Updates** - Updated repos appear at the top of the list

---

**Last Updated**: May 2026  
**Author**: Daud Ki  
**Version**: 1.0.0
