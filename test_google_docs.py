#!/usr/bin/env python3
"""
Test script to verify Google Docs integration
Run this locally to diagnose credential issues
"""

import os
import sys

# Add api directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'api'))

from google_docs_simple import get_credentials, create_google_doc

print("=" * 80)
print("TESTING GOOGLE DOCS INTEGRATION")
print("=" * 80)

# Test 1: Check if credentials can be loaded
print("\n1. Testing credential loading...")
creds = get_credentials()

if creds:
    print("✓ Credentials loaded successfully!")
    print(f"  Project ID: {creds.project_id if hasattr(creds, 'project_id') else 'N/A'}")
    print(f"  Service account email: {creds.service_account_email if hasattr(creds, 'service_account_email') else 'N/A'}")
else:
    print("✗ Failed to load credentials")
    print("\nTroubleshooting steps:")
    print("1. Check if GOOGLE_CREDENTIALS environment variable is set:")
    print(f"   Set: {'Yes' if os.environ.get('GOOGLE_CREDENTIALS') else 'No'}")
    print("2. Check if credentials.json file exists:")
    print(f"   Exists: {'Yes' if os.path.exists('credentials.json') else 'No'}")
    sys.exit(1)

# Test 2: Try to create a test document
print("\n2. Testing document creation...")
test_doc = create_google_doc(
    "Test Document - QA Generator",
    "This is a test document created by the QA Documentation Generator.\n\nIf you can see this, the integration is working!"
)

if test_doc:
    print("✓ Document created successfully!")
    print(f"  Document ID: {test_doc['id']}")
    print(f"  Document URL: {test_doc['url']}")
    print(f"  Document Title: {test_doc['title']}")
    print("\n✓ ALL TESTS PASSED! Google Docs integration is working.")
else:
    print("✗ Failed to create document")
    print("\nPossible issues:")
    print("1. Service account doesn't have permission to create documents")
    print("2. Google Docs API is not enabled")
    print("3. API quota exceeded")
    print("4. Network connectivity issues")

print("\n" + "=" * 80)
