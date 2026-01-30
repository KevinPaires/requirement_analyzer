# Deployment Guide - QA Documentation Generator

Quick guide to deploy your QA Documentation Generator website.

## 🚀 Quick Deploy (Frontend Only - GitHub Pages)

This is the fastest way to get started. The frontend will work with local file generation (no Google Docs integration).

### Steps:

1. **Push to GitHub**
   ```bash
   git init
   git add .
   git commit -m "Initial commit: QA Documentation Generator"
   git remote add origin https://github.com/yourusername/requirement_analyzer.git
   git push -u origin main
   ```

2. **Enable GitHub Pages**
   - Go to your repository on GitHub
   - Click "Settings"
   - Navigate to "Pages" in the left sidebar
   - Under "Source":
     - Branch: `main`
     - Folder: `/web`
   - Click "Save"

3. **Wait for deployment**
   - GitHub will build and deploy automatically
   - Check the Actions tab to see progress
   - Your site will be live at: `https://yourusername.github.io/requirement_analyzer`

**Note**: Without backend, the frontend will run in demo mode with example data.

---

## 🌐 Full Deploy (Frontend + Backend)

For full functionality with Google Docs integration, deploy both frontend and backend.

### Part 1: Deploy Frontend (GitHub Pages)

Follow the "Quick Deploy" steps above.

### Part 2: Deploy Backend (Heroku)

#### Prerequisites:
- Heroku account (free tier available)
- Heroku CLI installed
- Google Cloud credentials configured

#### Steps:

1. **Install Heroku CLI**
   ```bash
   # macOS
   brew tap heroku/brew && brew install heroku

   # Ubuntu/Debian
   curl https://cli-assets.heroku.com/install.sh | sh

   # Windows
   # Download from: https://devcenter.heroku.com/articles/heroku-cli
   ```

2. **Login to Heroku**
   ```bash
   heroku login
   ```

3. **Create Heroku app**
   ```bash
   heroku create your-qa-generator-api
   ```

4. **Configure Google API credentials**

   You need to convert your `credentials.json` to environment variables for Heroku:

   ```bash
   # Set the credentials as a Heroku config var
   heroku config:set GOOGLE_CREDENTIALS="$(cat credentials.json)"
   ```

5. **Deploy to Heroku**
   ```bash
   git push heroku main
   ```

6. **Verify deployment**
   ```bash
   heroku logs --tail
   heroku open
   ```

   Test the API:
   ```bash
   curl https://your-qa-generator-api.herokuapp.com/api/health
   ```

7. **Update frontend to use backend**

   Edit `web/script.js` and change:
   ```javascript
   const API_BASE_URL = 'https://your-qa-generator-api.herokuapp.com/api';
   ```

   Commit and push:
   ```bash
   git add web/script.js
   git commit -m "Update API URL for production"
   git push origin main
   ```

---

## 🔧 Alternative Backend Deployment Options

### Option 1: Railway.app

Railway offers automatic Python deployment with HTTPS.

1. Go to [Railway.app](https://railway.app)
2. Click "Start a New Project"
3. Connect your GitHub repository
4. Railway will auto-detect Python and deploy
5. Add environment variable: `GOOGLE_CREDENTIALS`
6. Get your deployment URL and update `web/script.js`

### Option 2: Render.com

Render offers free Python hosting.

1. Go to [Render.com](https://render.com)
2. Click "New +" → "Web Service"
3. Connect your GitHub repository
4. Configure:
   - Build Command: `cd api && pip install -r requirements.txt`
   - Start Command: `cd api && gunicorn app:app`
5. Add environment variable: `GOOGLE_CREDENTIALS`
6. Deploy and get your URL

### Option 3: Vercel (Frontend + Serverless Backend)

Vercel supports Python serverless functions.

1. Install Vercel CLI: `npm i -g vercel`
2. Create `api/` directory with your Flask app as serverless functions
3. Run `vercel` in project root
4. Follow prompts to deploy

---

## 🔐 Google Cloud Setup

For Google Docs/Sheets integration:

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Name it "QA Generator" and create

### 2. Enable APIs

1. In the Cloud Console, go to "APIs & Services" → "Library"
2. Search and enable:
   - Google Docs API
   - Google Sheets API
   - Google Drive API (optional, for file management)

### 3. Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. If prompted, configure OAuth consent screen:
   - User Type: External
   - App name: QA Generator
   - User support email: your email
   - Developer contact: your email
4. Application type: "Desktop app"
5. Name: "QA Generator Desktop"
6. Click "Create"
7. Download the JSON file
8. Rename to `credentials.json`

### 4. For Production (Web Application)

For Heroku/Railway deployment:

1. Create another OAuth client ID
2. Application type: "Web application"
3. Authorized redirect URIs:
   - `https://your-app.herokuapp.com/oauth2callback`
   - `http://localhost:5000/oauth2callback` (for local testing)
4. Download and use these credentials for production

---

## 🧪 Test Your Deployment

### Test Frontend

1. Visit your GitHub Pages URL
2. Click on example prompts
3. Verify UI loads correctly

### Test Backend

```bash
# Health check
curl https://your-api.herokuapp.com/api/health

# Generate documentation
curl -X POST https://your-api.herokuapp.com/api/generate \
  -H "Content-Type: application/json" \
  -d '{
    "requirement": "Login feature with email and password",
    "session_id": "test123"
  }'
```

### Test Full Integration

1. Open your GitHub Pages site
2. Paste sample requirements
3. Click "Generate"
4. Wait for Google Docs links
5. Click links to verify documents were created

---

## 🐛 Troubleshooting

### Frontend not loading
- Check GitHub Pages settings
- Verify `web/` folder contains `index.html`
- Check browser console for errors

### Backend 500 errors
- Check Heroku logs: `heroku logs --tail`
- Verify Google credentials are set
- Check Python version compatibility

### Google API errors
- Verify APIs are enabled in Cloud Console
- Check OAuth credentials are valid
- Ensure redirect URIs match your deployment URL

### CORS errors
- Verify Flask-CORS is installed
- Check API_BASE_URL in `web/script.js` is correct

---

## 📊 Monitoring

### Heroku Metrics

```bash
heroku logs --tail
heroku ps
heroku restart
```

### Check API Health

```bash
# Add to your monitoring
curl https://your-api.herokuapp.com/api/health
```

---

## 💰 Cost Estimates

### Free Tier (Recommended for testing)
- GitHub Pages: Free
- Heroku Free Tier: Free (sleeps after 30 min)
- Google Cloud: Free (limited quota)
- **Total: $0/month**

### Production Tier
- GitHub Pages: Free
- Heroku Hobby: $7/month
- Google Cloud: Pay-as-you-go (~$0-5/month for low usage)
- **Total: ~$7-12/month**

---

## 🎯 Next Steps

After successful deployment:

1. ✅ Test with real requirements
2. ✅ Share with your QA team
3. ✅ Collect feedback
4. ✅ Add custom test templates
5. ✅ Integrate with your CI/CD pipeline

---

## 📞 Support

If you encounter issues:

1. Check the [Troubleshooting](#troubleshooting) section
2. Review Heroku/Railway logs
3. Open an issue on GitHub
4. Contact: [your-email@example.com]

---

Good luck with your deployment! 🚀
