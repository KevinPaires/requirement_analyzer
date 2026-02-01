# Troubleshooting Google Docs Integration

## Current Status

The API is running successfully on Railway but returning demo links instead of real Google Docs. This guide will help diagnose and fix the issue.

## Step 1: Verify Service Account Credentials Format

Your service account JSON should look like this:

```json
{
  "type": "service_account",
  "project_id": "your-project-id",
  "private_key_id": "...",
  "private_key": "-----BEGIN PRIVATE KEY-----\n...\n-----END PRIVATE KEY-----\n",
  "client_email": "your-service-account@your-project.iam.gserviceaccount.com",
  "client_id": "...",
  "auth_uri": "https://accounts.google.com/o/oauth2/auth",
  "token_uri": "https://oauth2.googleapis.com/token",
  "auth_provider_x509_cert_url": "https://www.googleapis.com/oauth2/v1/certs",
  "client_x509_cert_url": "..."
}
```

**IMPORTANT**: This is different from OAuth Desktop credentials (which have `"installed"` key).

## Step 2: Check Railway Environment Variable

1. Go to Railway dashboard: https://railway.app
2. Select your project: web-production-f4c75
3. Click on "Variables" tab
4. Verify `GOOGLE_CREDENTIALS` is set
5. Click "View" to see the value
6. Confirm it contains the service account JSON (not OAuth credentials)

## Step 3: Check Railway Deployment Logs

After the latest deployment (with enhanced logging), check the logs:

1. Go to Railway dashboard
2. Click on "Deployments" tab
3. Click on the latest deployment
4. Look for these log messages:

### Successful Flow:
```
✓ Successfully imported google_docs_simple
Found GOOGLE_CREDENTIALS env var (length: 2345)
Parsed JSON, project: your-project-id
Successfully created service account credentials
Creating Test Plan doc: Feature Name - Test Plan
Attempting to create Google Doc: Feature Name - Test Plan
Building docs service...
Creating document...
Document created with ID: abc123xyz
✓ Test Plan created: https://docs.google.com/document/d/abc123xyz/edit
```

### Failed Flow (Credentials Not Found):
```
✓ Successfully imported google_docs_simple
No credentials found
✗ Test Plan creation returned None
```

### Failed Flow (Wrong Credentials Format):
```
✓ Successfully imported google_docs_simple
Found GOOGLE_CREDENTIALS env var (length: 234)
Error parsing GOOGLE_CREDENTIALS: Service account info was not in the expected format
No credentials found
✗ Test Plan creation returned None
```

### Failed Flow (API Not Enabled):
```
✓ Successfully imported google_docs_simple
Found GOOGLE_CREDENTIALS env var (length: 2345)
Parsed JSON, project: your-project-id
Successfully created service account credentials
Creating Test Plan doc: Feature Name - Test Plan
Attempting to create Google Doc: Feature Name - Test Plan
Error creating Google Doc: <HttpError 403 when requesting ... Google Docs API has not been used...>
```

## Step 4: Common Issues & Solutions

### Issue 1: Wrong Credentials Type

**Symptom**: Logs show "Service account info was not in the expected format"

**Solution**:
1. Go to Google Cloud Console: https://console.cloud.google.com
2. Select your project (scraper-484017)
3. Go to "IAM & Admin" → "Service Accounts"
4. Find or create a service account
5. Click on the service account email
6. Go to "Keys" tab
7. Click "Add Key" → "Create new key"
8. Choose "JSON" format
9. Download the file
10. Copy the entire JSON content
11. In Railway, update `GOOGLE_CREDENTIALS` variable with this JSON

### Issue 2: APIs Not Enabled

**Symptom**: Logs show "Google Docs API has not been used" or 403 error

**Solution**:
1. Go to Google Cloud Console: https://console.cloud.google.com
2. Select your project (scraper-484017)
3. Go to "APIs & Services" → "Library"
4. Search and enable these APIs:
   - Google Docs API
   - Google Sheets API
   - Google Drive API

### Issue 3: Service Account Permissions

**Symptom**: Logs show "Permission denied" or 403 error after APIs are enabled

**Solution**:
Service accounts can create documents in their own Drive, but you won't see them in your personal Drive. You have two options:

**Option A: Use a shared folder** (Recommended)
1. Create a folder in your Google Drive
2. Right-click → Share
3. Add your service account email (looks like: name@project-id.iam.gserviceaccount.com)
4. Give it "Editor" access
5. Modify the code to create documents in this folder

**Option B: Share individual documents**
- After creation, the service account needs to share each document with you
- This happens automatically if you modify the code (see below)

### Issue 4: Documents Created But Not Visible

**Symptom**: Logs show documents created successfully, but you can't find them

**Explanation**: Service accounts have their own Drive space separate from your personal Drive.

**Solution**: Add sharing after document creation.

Update `/Users/kevinpaires/requirment_analyzer/api/google_docs_simple.py`:

```python
def create_google_doc(title, content):
    """Create a Google Doc with content"""
    try:
        # ... existing code ...

        doc_id = doc.get('documentId')
        print(f"Document created with ID: {doc_id}")

        # Share the document with a specific email (ADD THIS)
        drive_service = build('drive', 'v3', credentials=creds)
        drive_service.permissions().create(
            fileId=doc_id,
            body={
                'type': 'anyone',
                'role': 'writer',
                'withLink': True
            }
        ).execute()
        print(f"Document shared with anyone who has the link")

        # ... rest of existing code ...
```

## Step 5: Test the API Again

After making changes:

1. Wait for Railway to redeploy (2-3 minutes)
2. Test the API:
   ```bash
   curl -X POST https://web-production-f4c75.up.railway.app/api/generate \
     -H "Content-Type: application/json" \
     -d '{"requirement": "Test Feature", "session_id": "debug"}'
   ```
3. Check if real Google Docs URLs are returned (not demo links)
4. Try opening the URLs in your browser

## Step 6: Check Google Cloud Quota

If everything looks correct but documents aren't being created:

1. Go to Google Cloud Console
2. Navigate to "APIs & Services" → "Dashboard"
3. Check if you've exceeded any quotas
4. Default quota is usually 100 requests per 100 seconds (plenty for normal use)

## Quick Checklist

- [ ] Service account JSON format is correct (has `client_email` and `token_uri`)
- [ ] `GOOGLE_CREDENTIALS` environment variable is set in Railway
- [ ] Google Docs API is enabled in Google Cloud
- [ ] Google Sheets API is enabled in Google Cloud
- [ ] Google Drive API is enabled in Google Cloud
- [ ] Service account has "Owner" or "Editor" role on the project
- [ ] Railway has deployed the latest code with enhanced logging
- [ ] API returns real Google Docs URLs (not demo links)

## Next Steps

1. Check Railway deployment logs (should have new messages now)
2. Share the relevant log output (copy the section with the ✓ and ✗ symbols)
3. Based on the logs, we can identify the exact issue and fix it

## Need More Help?

If you're still having issues:

1. Go to Railway dashboard
2. Click on your deployment
3. Copy the logs from a failed generation attempt
4. Share the logs (focus on lines with "Google" or "Error")
5. We'll identify the exact problem and fix it
