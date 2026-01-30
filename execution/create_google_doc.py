#!/usr/bin/env python3
"""
Create and format Google Docs for QA deliverables.

This script handles authentication with Google API and creates
professionally formatted documents for Test Plans, Test Cases,
and Exploratory Testing Charters.
"""

import os
import json
from datetime import datetime
from typing import Dict, List, Any, Optional
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

# If modifying these scopes, delete token.json
SCOPES = ['https://www.googleapis.com/auth/documents',
          'https://www.googleapis.com/auth/drive.file']


class GoogleDocsCreator:
    """Handles Google Docs creation and formatting."""

    def __init__(self, credentials_file: str = 'credentials.json',
                 token_file: str = 'token.json'):
        """Initialize with Google API credentials."""
        self.credentials_file = credentials_file
        self.token_file = token_file
        self.creds = None
        self.docs_service = None
        self.drive_service = None
        self._authenticate()

    def _authenticate(self):
        """Authenticate with Google API."""
        # Check if token.json exists with valid credentials
        if os.path.exists(self.token_file):
            self.creds = Credentials.from_authorized_user_file(
                self.token_file, SCOPES
            )

        # If no valid credentials, let user log in
        if not self.creds or not self.creds.valid:
            if self.creds and self.creds.expired and self.creds.refresh_token:
                self.creds.refresh(Request())
            else:
                if not os.path.exists(self.credentials_file):
                    raise FileNotFoundError(
                        f"Credentials file not found: {self.credentials_file}\n"
                        "Please download from Google Cloud Console."
                    )
                flow = InstalledAppFlow.from_client_secrets_file(
                    self.credentials_file, SCOPES
                )
                self.creds = flow.run_local_server(port=0)

            # Save credentials for next run
            with open(self.token_file, 'w') as token:
                token.write(self.creds.to_json())

        # Build services
        self.docs_service = build('docs', 'v1', credentials=self.creds)
        self.drive_service = build('drive', 'v3', credentials=self.creds)

    def create_document(self, title: str) -> Dict[str, str]:
        """
        Create a new Google Doc.

        Args:
            title: Document title

        Returns:
            Dict with 'document_id' and 'document_url'
        """
        try:
            document = self.docs_service.documents().create(
                body={'title': title}
            ).execute()

            doc_id = document.get('documentId')
            doc_url = f"https://docs.google.com/document/d/{doc_id}/edit"

            return {
                'document_id': doc_id,
                'document_url': doc_url,
                'title': title
            }
        except HttpError as error:
            raise Exception(f"Error creating document: {error}")

    def insert_text(self, document_id: str, text: str, index: int = 1):
        """Insert text at specified index."""
        requests = [{
            'insertText': {
                'location': {'index': index},
                'text': text
            }
        }]
        self.docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()

    def apply_formatting(self, document_id: str, requests: List[Dict]):
        """Apply formatting requests to document."""
        try:
            self.docs_service.documents().batchUpdate(
                documentId=document_id,
                body={'requests': requests}
            ).execute()
        except HttpError as error:
            raise Exception(f"Error applying formatting: {error}")

    def insert_table(self, document_id: str, rows: int, columns: int,
                    index: int = 1) -> Dict:
        """
        Insert a table at specified index.

        Args:
            document_id: Google Doc ID
            rows: Number of rows
            columns: Number of columns
            index: Position to insert

        Returns:
            Dict with table insertion details
        """
        requests = [{
            'insertTable': {
                'rows': rows,
                'columns': columns,
                'location': {'index': index}
            }
        }]

        result = self.docs_service.documents().batchUpdate(
            documentId=document_id,
            body={'requests': requests}
        ).execute()

        return result

    def create_test_plan(self, title: str, content: Dict[str, Any]) -> Dict[str, str]:
        """
        Create a formatted Test Plan document.

        Args:
            title: Document title
            content: Dict with sections like 'introduction', 'scope', etc.

        Returns:
            Dict with document_id and document_url
        """
        doc_info = self.create_document(title)
        doc_id = doc_info['document_id']

        # Build document content
        sections = []

        # Header
        sections.append(f"{title}\n\n")

        # Document Control
        if 'document_control' in content:
            sections.append("Document Control\n")
            dc = content['document_control']
            sections.append(f"Version: {dc.get('version', 'v1.0')}\n")
            sections.append(f"Date Created: {dc.get('date_created', datetime.now().strftime('%Y-%m-%d'))}\n")
            sections.append(f"Author: {dc.get('author', 'QA Team')}\n\n")

        # Introduction & Scope
        if 'introduction' in content:
            sections.append("1. Introduction & Scope\n")
            sections.append(f"{content['introduction']}\n\n")

        if 'scope' in content:
            sections.append("In Scope:\n")
            for item in content['scope'].get('in_scope', []):
                sections.append(f"  • {item}\n")
            sections.append("\nOut of Scope:\n")
            for item in content['scope'].get('out_of_scope', []):
                sections.append(f"  • {item}\n")
            sections.append("\n")

        # Test Strategy
        if 'test_strategy' in content:
            sections.append("2. Test Strategy\n")
            sections.append(f"{content['test_strategy']}\n\n")

        # Risk Analysis
        if 'risks' in content:
            sections.append("3. Risk Analysis\n")
            for risk in content['risks']:
                sections.append(f"  • {risk}\n")
            sections.append("\n")

        # Insert all text
        full_text = "".join(sections)
        self.insert_text(doc_id, full_text)

        # Apply formatting (headers, bold, etc.)
        # This is simplified - you can add more complex formatting

        return doc_info

    def create_test_cases_doc(self, title: str, test_cases: List[Dict]) -> Dict[str, str]:
        """
        Create a Test Cases document with table.

        Args:
            title: Document title
            test_cases: List of test case dictionaries

        Returns:
            Dict with document_id and document_url
        """
        doc_info = self.create_document(title)
        doc_id = doc_info['document_id']

        # Insert title
        self.insert_text(doc_id, f"{title}\n\n")

        # Create table
        # Header row + test case rows
        num_rows = len(test_cases) + 1
        num_columns = 12  # TC ID, Description, Category, Precondition, Test Data, Steps, Expected, Actual, Pass/Fail, Bug ID, Priority, Technique

        # Note: Actually populating table cells requires more complex API calls
        # This is a placeholder for the table structure
        self.insert_table(doc_id, num_rows, num_columns, index=len(title) + 3)

        return doc_info

    def save_backup(self, filename: str, data: Dict):
        """Save backup JSON in .tmp/ directory."""
        os.makedirs('.tmp', exist_ok=True)
        filepath = os.path.join('.tmp', filename)
        with open(filepath, 'w') as f:
            json.dump(data, f, indent=2)
        return filepath


def main():
    """Example usage."""
    import sys

    if len(sys.argv) < 3:
        print("Usage: python create_google_doc.py <doc_type> <title>")
        print("  doc_type: test_plan | test_cases | exploratory")
        sys.exit(1)

    doc_type = sys.argv[1]
    title = sys.argv[2]

    creator = GoogleDocsCreator()

    if doc_type == 'test_plan':
        content = {
            'document_control': {
                'version': 'v1.0',
                'date_created': datetime.now().strftime('%Y-%m-%d'),
                'author': 'QA Team'
            },
            'introduction': 'This test plan covers...',
            'scope': {
                'in_scope': ['Feature A', 'Feature B'],
                'out_of_scope': ['Legacy system', 'Third-party integrations']
            }
        }
        result = creator.create_test_plan(title, content)
    elif doc_type == 'test_cases':
        test_cases = []  # Would be populated with actual test cases
        result = creator.create_test_cases_doc(title, test_cases)
    else:
        result = creator.create_document(title)

    print(f"Document created successfully!")
    print(f"Document ID: {result['document_id']}")
    print(f"Document URL: {result['document_url']}")

    # Save backup
    backup_file = f"{doc_type}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    backup_path = creator.save_backup(backup_file, result)
    print(f"Backup saved: {backup_path}")


if __name__ == '__main__':
    main()
