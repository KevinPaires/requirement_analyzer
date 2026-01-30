#!/usr/bin/env python3
"""
Populate existing Google Docs with content from markdown files.
"""

import os
import sys
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = ['https://www.googleapis.com/auth/documents']


def authenticate():
    """Authenticate with Google API."""
    creds = None
    token_file = 'token.json'

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        print("Error: Invalid credentials. Please run create_google_doc.py first.")
        sys.exit(1)

    return build('docs', 'v1', credentials=creds)


def insert_text_to_doc(service, document_id, text):
    """Insert text into a Google Doc."""
    try:
        # Insert text at the beginning (index 1)
        requests = [{
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': text
            }
        }]

        result = service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()

        return result
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def main():
    if len(sys.argv) != 3:
        print("Usage: python populate_google_doc.py <document_id> <markdown_file_path>")
        sys.exit(1)

    document_id = sys.argv[1]
    markdown_file = sys.argv[2]

    # Read markdown file
    if not os.path.exists(markdown_file):
        print(f"Error: File not found: {markdown_file}")
        sys.exit(1)

    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    # Authenticate
    service = authenticate()

    # Insert content
    print(f"Inserting content into document {document_id}...")
    result = insert_text_to_doc(service, document_id, content)

    if result:
        print("✅ Content inserted successfully!")
        print(f"View document: https://docs.google.com/document/d/{document_id}/edit")
    else:
        print("❌ Failed to insert content")
        sys.exit(1)


if __name__ == '__main__':
    main()
