# Fixing 403 "The caller does not have permission" Error

## The Problem

Your service account is authenticated correctly (credentials load successfully), but it's getting a 403 error when trying to create documents:

```
HttpError 403: "The caller does not have permission"
```

This error occurs BEFORE we even try to share the document, meaning the service account can't create documents at all.

## Root Cause

Service accounts need TWO things:
1. ✅ **API Enabled** - You've done this (Google Docs API, Google Sheets API)
2. ❌ **Proper IAM Role** - This is likely missing

Even though the service account has "Owner" role on the PROJECT, Google Workspace APIs (Docs, Sheets) require different permissions.

## Solution: Enable Google Workspace APIs for Service Account

### Step 1: Verify APIs are Enabled

1. Go to: https://console.cloud.google.com/apis/dashboard?project=scraper-484017
2. Check that these are enabled:
   - Google Docs API
   - Google Sheets API
   - Google Drive API

If any say "Enable", click to enable them.

### Step 2: Check Service Account Permissions

The service account email is: `qa-generator-services@scraper-484017.iam.gserviceaccount.com`

1. Go to: https://console.cloud.google.com/iam-admin/iam?project=scraper-484017
2. Find `qa-generator-services@scraper-484017.iam.gserviceaccount.com`
3. Check its roles

**Required roles:**
- ✅ Project > Owner (you already have this)

### Step 3: Try Creating New Service Account (If Above Doesn't Work)

Sometimes service accounts get in a weird state. Let's create a fresh one:

1. Go to: https://console.cloud.google.com/iam-admin/serviceaccounts?project=scraper-484017

2. Click "Create Service Account"

3. Fill in:
   - Name: `qa-docs-generator`
   - Description: `Service account for QA Documentation Generator`
   - Click "Create and Continue"

4. Grant roles:
   - Select "Project > Editor" role
   - Click "Continue"

5. Click "Done"

6. Click on the newly created service account

7. Go to "Keys" tab

8. Click "Add Key" > "Create new key"

9. Select "JSON"

10. Download the file

11. Open the JSON file and copy ALL the content

12. Go to Railway dashboard: https://railway.app/project/<your-project-id>

13. Click "Variables"

14. Find `GOOGLE_CREDENTIALS` and click "Edit"

15. Paste the entire JSON content

16. Click "Save"

17. Wait 2-3 minutes for Railway to redeploy

### Step 4: Test Again

After Railway redeploys, test:

```bash
curl -X POST https://web-production-f4c75.up.railway.app/api/generate \
  -H "Content-Type: application/json" \
  -d '{"requirement": "Test feature", "session_id": "test"}' | python3 -m json.tool
```

Look for real Google Docs URLs instead of demo links.

## Alternative: Verify API Status Directly

Run this to check if APIs are enabled:

1. Go to: https://console.cloud.google.com/apis/library/docs.googleapis.com?project=scraper-484017
   - Should say "API enabled" with a "Manage" button

2. Go to: https://console.cloud.google.com/apis/library/sheets.googleapis.com?project=scraper-484017
   - Should say "API enabled" with a "Manage" button

3. Go to: https://console.cloud.google.com/apis/library/drive.googleapis.com?project=scraper-484017
   - Should say "API enabled" with a "Manage" button

If any say "Enable API", click it.

## What If It Still Doesn't Work?

The 403 error specifically on document creation (not on sharing) usually means one of:

1. **APIs not actually enabled** - Double-check the links above
2. **Service account in wrong project** - Verify the service account is in project `scraper-484017`
3. **Google Workspace domain restrictions** - If you're using Google Workspace (not regular Gmail), there might be admin restrictions
4. **API quota exceeded** - Check: https://console.cloud.google.com/apis/api/docs.googleapis.com/quotas?project=scraper-484017

## Expected Success

When working, you should see:

```json
{
  "test_plan": {
    "id": "1a2b3c4d5e6f7g8h9i0j",
    "title": "Test feature - Test Plan",
    "url": "https://docs.google.com/document/d/1a2b3c4d5e6f7g8h9i0j/edit"
  },
  ...
}
```

NOT:

```json
{
  "test_plan": {
    "id": "demo",
    "url": "https://docs.google.com/document/d/demo",
    ...
  },
  ...
}
```

## Need More Help?

Check Railway logs:
1. Go to Railway dashboard
2. Click on your deployment
3. Look for lines with "✓" or "✗"
4. Share any error messages you see

The most likely fix is creating a new service account with Editor role.
