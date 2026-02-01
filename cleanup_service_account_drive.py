#!/usr/bin/env python3
"""
Cleanup script to delete all files from service account's Google Drive
Run this to free up storage quota
"""

import sys
import os

# Add api directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from google_docs_simple import get_credentials
from googleapiclient.discovery import build

print("=" * 80)
print("GOOGLE DRIVE CLEANUP - Service Account")
print("=" * 80)

# Get credentials
creds = get_credentials()
if not creds:
    print("❌ Could not load credentials")
    sys.exit(1)

print(f"✓ Credentials loaded: {creds.service_account_email}")
print("\nConnecting to Google Drive...")

drive_service = build('drive', 'v3', credentials=creds)

# List all files
print("\nFetching list of files in service account's Drive...")
results = drive_service.files().list(
    pageSize=1000,
    fields="files(id, name, mimeType, createdTime, size)"
).execute()

files = results.get('files', [])

if not files:
    print("\n✓ No files found. Drive is already clean!")
    sys.exit(0)

print(f"\nFound {len(files)} files:")
print("-" * 80)

total_size = 0
for f in files:
    size = int(f.get('size', 0))
    total_size += size
    size_mb = size / (1024 * 1024)
    print(f"  {f['name'][:50]:50} {size_mb:8.2f} MB")

print("-" * 80)
print(f"Total size: {total_size / (1024 * 1024):.2f} MB ({total_size / (1024 * 1024 * 1024):.2f} GB)")

# Ask for confirmation
print("\n⚠️  WARNING: This will DELETE ALL files from the service account's Drive!")
response = input("Do you want to proceed? (yes/no): ")

if response.lower() != 'yes':
    print("Cancelled.")
    sys.exit(0)

# Delete all files
print("\nDeleting files...")
deleted = 0
failed = 0

for f in files:
    try:
        drive_service.files().delete(fileId=f['id']).execute()
        print(f"  ✓ Deleted: {f['name']}")
        deleted += 1
    except Exception as e:
        print(f"  ✗ Failed to delete {f['name']}: {e}")
        failed += 1

print("\n" + "=" * 80)
print(f"Cleanup complete!")
print(f"  Deleted: {deleted} files")
print(f"  Failed: {failed} files")
print(f"  Freed: ~{total_size / (1024 * 1024):.2f} MB")
print("=" * 80)
