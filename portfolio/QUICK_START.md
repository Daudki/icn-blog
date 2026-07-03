# 🚀 GitHub Portfolio Integration - Quick Start

## What You Just Got

Your portfolio now features **real-time GitHub repository integration**! Every time you add a new repository to GitHub, it automatically appears on your portfolio.

## ⚡ Quick Setup (30 seconds)

### Step 1: Open the GitHub Integration Script
Open: `js/github-integration.js`

### Step 2: Update Your GitHub Username (Line 9)
```javascript
const GITHUB_USERNAME = 'kisulodaud'; // ⬅️ CHANGE THIS to your GitHub username
```

### Step 3: Done! 🎉
That's it! Your portfolio will now display all your public GitHub repositories.

## 🎯 Common Tasks

### Enable Auto-Refresh (Recommended)
Your portfolio will automatically check for new repos every 5 minutes.

**In `js/github-integration.js`, find the bottom section and uncomment:**
```javascript
setupAutoRefresh(); // Uncomment to enable
```

### View Specific Number of Repos
To show only your last 20 repos instead of all:
```javascript
const CONFIG = {
    maxRepos: 20,  // Change from 100 to 20
};
```

### Sort By Stars (Most Popular First)
```javascript
const CONFIG = {
    sortBy: 'stars',  // Instead of 'updated'
};
```

### Include Forked Repositories
```javascript
const CONFIG = {
    includeForked: true,  // Default: false
};
```

### Enable Debug Console Logging
```javascript
const CONFIG = {
    debug: true,  // See all actions in browser console
};
```

## 📊 What Gets Displayed

For each repository, your portfolio shows:
- 📝 **Repository Name** - Your project title
- 📄 **Description** - From the repo description
- 🏷️ **Language Tags** - Programming language (color-coded)
- 📚 **Topics** - Up to 3 tags you've added to the repo
- ⭐ **Stars** - Number of GitHub stars
- 🔀 **Forks** - Number of times cloned
- 📅 **Last Updated** - When you last updated it
- 🔗 **Direct Links** - To GitHub repo and clone URL

## 🎨 Customization Options

### Language Colors
Add or modify language colors in `js/github-integration.js` (around line 60):
```javascript
const languageColors = {
    'MyLanguage': '#color-code',
    // Add your languages here
};
```

### API Rate Limiting
GitHub allows:
- **60 requests/hour** (unauthenticated)
- **5,000 requests/hour** (with token)

Since you only fetch once per load, you're well within limits.

## 🔄 How Auto-Refresh Works

When enabled, auto-refresh:
1. Updates repos every 5 minutes
2. Updates when you return to the portfolio tab
3. Caches results for 30 minutes
4. Falls back to cache if GitHub is down

## 📱 Responsive & Mobile-Friendly
- ✅ Works on desktop (multi-column grid)
- ✅ Works on tablets (2-column layout)
- ✅ Works on mobile (single column)
- ✅ Images lazy-load for performance

## 🛠️ Troubleshooting

### Repos Not Showing?
1. Check **browser console** (F12) for errors
2. Verify your **GitHub username** is correct
3. Ensure repos are **public** (private repos won't show)
4. Check internet connection

### Showing Old Data?
1. **Hard refresh** browser (Ctrl+Shift+R or Cmd+Shift+R)
2. Clear **browser cache**
3. Check that repos aren't in draft status on GitHub

### Want Real-Time Updates?
The current solution refreshes every 5 minutes (or when you visit). For truly real-time updates, you'd need:
- GitHub Webhooks setup
- Backend server to receive notifications
- This is an advanced setup - reach out if needed

## 📚 Files Modified

- ✨ **`js/github-integration.js`** - NEW: GitHub API integration
- 📝 **`index.html`** - Updated projects section
- 🎨 **`css/style.css`** - Added animations and styling

## 🎓 Learn More

**Full Documentation**: Read `GITHUB_INTEGRATION_GUIDE.md` for advanced features and configuration.

**GitHub API Docs**: https://docs.github.com/en/rest/repos

## 🚨 Important Notes

- Your portfolio fetches public API data - no authentication required
- Repos with 0 stars/forks still display beautifully
- Topics/tags from your repo are automatically pulled in
- Images are dynamically selected based on language type
- Placeholder images for repos without descriptions

## 💡 Pro Tips

1. **Write good descriptions** - They show on your portfolio
2. **Add GitHub topics** - They appear as tags on cards
3. **Keep repos updated** - Recently updated repos appear first
4. **Star your best work** - Star count displays prominently
5. **Use consistent naming** - Makes portfolios look professional

## ✅ Verification Checklist

- [ ] Updated GitHub username in `js/github-integration.js`
- [ ] Tested portfolio loads without errors
- [ ] At least one public repo shows up
- [ ] Clicked "View Repo" - links to GitHub correctly
- [ ] (Optional) Enabled auto-refresh for live updates

## 🎯 Next Steps

1. ✅ Save your changes
2. ✅ Reload your portfolio in browser
3. ✅ Watch your GitHub repos load automatically!
4. ✅ (Optional) Enable auto-refresh
5. ✅ Share your portfolio - it's now up-to-date!

---

**Questions?** Check the full guide at `GITHUB_INTEGRATION_GUIDE.md`

**Last Updated**: May 2026
