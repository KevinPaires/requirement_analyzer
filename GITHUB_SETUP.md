# GitHub Setup - Quick Start Guide

Follow these steps to get your QA Generator website live on GitHub Pages in 5 minutes.

## 📋 Prerequisites

- GitHub account
- Git installed locally
- Terminal/Command Prompt access

## 🚀 Step-by-Step Setup

### 1. Create GitHub Repository

```bash
# Option A: Create via GitHub website
# Go to github.com → New Repository → Name: "requirement_analyzer"

# Option B: Create via GitHub CLI (if installed)
gh repo create requirement_analyzer --public
```

### 2. Initialize and Push Your Code

```bash
# Navigate to your project directory
cd /Users/kevinpaires/requirment_analyzer

# Initialize git (if not already)
git init

# Add all files
git add .

# Commit
git commit -m "Initial commit: QA Documentation Generator

- Modern ChatGPT-style UI
- Flask REST API backend
- Google Docs/Sheets integration
- Boundary value analysis test cases
- Complete documentation"

# Add remote (replace 'yourusername' with your GitHub username)
git remote add origin https://github.com/yourusername/requirement_analyzer.git

# Push to GitHub
git push -u origin main
```

### 3. Enable GitHub Pages

**Via GitHub Website:**

1. Go to your repository on GitHub
2. Click **Settings** tab
3. Scroll to **Pages** section (left sidebar)
4. Under **Source**:
   - Branch: `main`
   - Folder: `/web` ← **IMPORTANT: Select /web, not root**
5. Click **Save**
6. Wait 1-2 minutes for deployment

**Your site will be live at:**
```
https://yourusername.github.io/requirement_analyzer
```

### 4. Test Your Deployment

Open your site and test:
- ✅ Welcome screen loads
- ✅ Example buttons work
- ✅ Can type in text area
- ✅ UI is responsive on mobile

**Note**: Without backend deployment, the app runs in demo mode (no Google Docs integration yet).

## 🔧 Optional: Deploy Backend

See [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for full backend deployment instructions.

### Quick Heroku Deploy

```bash
# Install Heroku CLI
brew install heroku/brew/heroku

# Login
heroku login

# Create app
heroku create your-qa-generator-api

# Add credentials
heroku config:set GOOGLE_CREDENTIALS="$(cat credentials.json)"

# Deploy
git push heroku main

# Update frontend API URL
# Edit web/script.js line 2:
# const API_BASE_URL = 'https://your-qa-generator-api.herokuapp.com/api';

# Commit and push
git add web/script.js
git commit -m "Update API URL for production"
git push origin main
```

## 📁 What Gets Deployed

From your `/web` folder:
- `index.html` - Main application interface
- `styles.css` - Modern styling
- `script.js` - Frontend logic
- `demo.html` - Optional landing page

## 🐛 Troubleshooting

### "Page not found" error
- Check Settings → Pages → Source is set to `main` branch, `/web` folder
- Wait 2-3 minutes after enabling Pages
- Clear browser cache

### Changes not appearing
- Go to repository → Actions tab
- Check deployment status
- Force refresh: Ctrl+Shift+R (Windows) or Cmd+Shift+R (Mac)

### Blank page
- Open browser console (F12)
- Check for JavaScript errors
- Verify all files are in `/web` folder

## 🎯 Next Steps

After your site is live:

1. Share URL with your QA team
2. Test with real requirements
3. Deploy backend for Google Docs integration
4. Add to your portfolio/resume
5. Star the repo ⭐

## 📞 Need Help?

- Check [WEB_README.md](WEB_README.md) for full documentation
- Review [DEPLOYMENT_GUIDE.md](DEPLOYMENT_GUIDE.md) for backend setup
- Open an issue on GitHub

---

**Congratulations! Your QA Generator is now live!** 🎉
