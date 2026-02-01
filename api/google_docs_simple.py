"""
Simple Google Docs integration for Railway deployment
"""
import os
import json
from google.oauth2 import service_account
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/documents',
    'https://www.googleapis.com/auth/drive',
    'https://www.googleapis.com/auth/spreadsheets'
]

def get_credentials():
    """Get credentials from environment variable or file"""
    # Try environment variable first (for Railway)
    creds_json = os.environ.get('GOOGLE_CREDENTIALS')

    if creds_json:
        try:
            # Parse JSON from environment
            print(f"Found GOOGLE_CREDENTIALS env var (length: {len(creds_json)})")
            creds_dict = json.loads(creds_json)
            print(f"Parsed JSON, project: {creds_dict.get('project_id')}")
            credentials = service_account.Credentials.from_service_account_info(
                creds_dict, scopes=SCOPES
            )
            print("Successfully created service account credentials")
            return credentials
        except Exception as e:
            print(f"Error parsing GOOGLE_CREDENTIALS: {e}")
            return None

    # Fallback to file (for local development)
    creds_file = 'credentials.json'
    if os.path.exists(creds_file):
        print(f"Using credentials file: {creds_file}")
        credentials = service_account.Credentials.from_service_account_file(
            creds_file, scopes=SCOPES
        )
        return credentials

    print("No credentials found")
    return None

def create_google_doc(title, content):
    """Create a Google Doc with content"""
    try:
        print(f"Attempting to create Google Doc: {title}")
        creds = get_credentials()
        if not creds:
            error_msg = "No credentials available"
            print(error_msg)
            return {'error': error_msg}

        print("Building services...")
        docs_service = build('docs', 'v1', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)

        # Create document
        print("Creating document...")
        doc = docs_service.documents().create(body={'title': title}).execute()
        doc_id = doc.get('documentId')
        print(f"Document created with ID: {doc_id}")

        # Make the document publicly accessible
        print("Sharing document...")
        drive_service.permissions().create(
            fileId=doc_id,
            body={
                'type': 'anyone',
                'role': 'writer'
            },
            fields='id'
        ).execute()
        print("Document shared with anyone who has the link")

        # Add content
        print("Adding content...")
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

        print(f"Successfully created doc: {doc_id}")
        return {
            'id': doc_id,
            'url': f'https://docs.google.com/document/d/{doc_id}/edit',
            'title': title
        }

    except Exception as e:
        error_msg = f'Error creating Google Doc: {e}'
        print(error_msg)
        import traceback
        traceback.print_exc()
        return {'error': error_msg}

def create_google_sheet(title, csv_data):
    """Create a Google Sheet with CSV data"""
    try:
        creds = get_credentials()
        if not creds:
            error_msg = "No credentials available"
            print(error_msg)
            return {'error': error_msg}

        sheets_service = build('sheets', 'v4', credentials=creds)
        drive_service = build('drive', 'v3', credentials=creds)

        # Create spreadsheet
        spreadsheet = {
            'properties': {'title': title}
        }

        sheet = sheets_service.spreadsheets().create(
            body=spreadsheet
        ).execute()

        sheet_id = sheet.get('spreadsheetId')

        # Make the spreadsheet publicly accessible
        print(f"Sharing spreadsheet {sheet_id}...")
        drive_service.permissions().create(
            fileId=sheet_id,
            body={
                'type': 'anyone',
                'role': 'writer'
            },
            fields='id'
        ).execute()
        print("Spreadsheet shared with anyone who has the link")

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
        error_msg = f'Error creating Google Sheet: {e}'
        print(error_msg)
        return {'error': error_msg}
