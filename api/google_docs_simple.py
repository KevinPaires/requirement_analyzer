"""
Simple Google Docs integration for Railway deployment
"""
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive.file',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_credentials():
    """Get credentials from environment variable or file"""
    # Try environment variable first (for Railway)
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')

    if creds_json:
        # Parse JSON from environment
        creds_dict = json.loads(creds_json)
        credentials = service_account.Credentials.from_service_account_info(
            creds_dict, scopes=SCOPES
        )
        return credentials

    # Fallback to file (for local development)
    creds_file = 'credentials.json'
    if os.path.exists(creds_file):
        credentials = service_account.Credentials.from_service_account_file(
            creds_file, scopes=SCOPES
        )
        return credentials

    return None

def create_google_doc(title, content):
    """Create a Google Doc with content"""
    try:
        creds = get_credentials()
        if not creds:
            return None

        docs_service = build('docs', 'v1', credentials=creds)

        # Create document
        doc = docs_service.documents().create(body={'title': title}).execute()
        doc_id = doc.get('documentId')

        # Add content
        requests = [{
            'insertText': {
                'location': {'index': 1},
                'text': content
            }
        }]

        docs_service.documents().batchUpdate(
            documentId=doc_id,
            body={'requests': requests}
        ).execute()

        return {
            'id': doc_id,
            'url': f'https://docs.google.com/document/d/{doc_id}/edit',
            'title': title
        }

    except Exception as e:
        print(f'Error creating Google Doc: {e}')
        return None

def create_google_sheet(title, csv_data):
    """Create a Google Sheet with CSV data"""
    try:
        creds = get_credentials()
        if not creds:
            return None

        sheets_service = build('sheets', 'v4', credentials=creds)

        # Create spreadsheet
        spreadsheet = {
            'properties': {'title': title}
        }

        sheet = sheets_service.spreadsheets().create(
            body=spreadsheet
        ).execute()

        sheet_id = sheet.get('spreadsheetId')

        # Add data (parse CSV)
        import csv
        import io
        reader = csv.reader(io.StringIO(csv_data))
        values = list(reader)

        sheets_service.spreadsheets().values().update(
            spreadsheetId=sheet_id,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body={'values': values}
        ).execute()

        # Format header row
        requests = [{
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {'red': 0.2, 'green': 0.2, 'blue': 0.2},
                        'textFormat': {
                            'foregroundColor': {'red': 1.0, 'green': 1.0, 'blue': 1.0},
                            'bold': True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        }]

        sheets_service.spreadsheets().batchUpdate(
            spreadsheetId=sheet_id,
            body={'requests': requests}
        ).execute()

        return {
            'id': sheet_id,
            'url': f'https://docs.google.com/spreadsheets/d/{sheet_id}/edit',
            'title': title
        }

    except Exception as e:
        print(f'Error creating Google Sheet: {e}')
        return None
