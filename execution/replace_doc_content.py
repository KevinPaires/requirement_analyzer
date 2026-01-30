#!/usr/bin/env python3
"""
Replace entire content of a Google Doc.
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
        print("Error: Invalid credentials")
        sys.exit(1)

    return build('docs', 'v1', credentials=creds)


def replace_content(service, document_id, new_content):
    """Replace all content in document with new content."""
    try:
        # Get current document to find end index
        doc = service.documents().get(documentId=document_id).execute()
        content = doc.get('body').get('content')
        end_index = content[-1].get('endIndex') - 1

        # Delete all existing content (except the last newline)
        requests = [{
            'deleteContentRange': {
                'range': {
                    'startIndex': 1,
                    'endIndex': end_index
                }
            }
        }]

        service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()

        # Insert new content
        requests = [{
            'insertText': {
                'location': {
                    'index': 1,
                },
                'text': new_content
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
        print("Usage: python replace_doc_content.py <document_id> <markdown_file>")
        sys.exit(1)

    document_id = sys.argv[1]
    markdown_file = sys.argv[2]

    if not os.path.exists(markdown_file):
        print(f"Error: File not found: {markdown_file}")
        sys.exit(1)

    with open(markdown_file, 'r', encoding='utf-8') as f:
        content = f.read()

    service = authenticate()
    print(f"Replacing content in document {document_id}...")

    result = replace_content(service, document_id, content)

    if result:
        print("✅ Content replaced successfully!")
        print(f"View: https://docs.google.com/document/d/{document_id}/edit")
    else:
        print("❌ Failed to replace content")
        sys.exit(1)


if __name__ == '__main__':
    main()
