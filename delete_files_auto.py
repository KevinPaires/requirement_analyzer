#!/usr/bin/env python3
"""Auto-delete all files from service account's Drive"""
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))
from google_docs_simple import get_credentials
from googleapiclient.discovery import build

creds = get_credentials()
if not creds:
    print("Could not load credentials")
    sys.exit(1)

drive_service = build('drive', 'v3', credentials=creds)
results = drive_service.files().list(pageSize=1000, fields="files(id, name)").execute()
files = results.get('files', [])

print(f"Found {len(files)} files. Deleting...")
for f in files:
    try:
        drive_service.files().delete(fileId=f['id']).execute()
        print(f"✓ Deleted: {f['name']}")
    except Exception as e:
        print(f"✗ Failed: {f['name']} - {e}")

print("Done!")
