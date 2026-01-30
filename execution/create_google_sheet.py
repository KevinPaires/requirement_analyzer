#!/usr/bin/env python3
"""
Create Google Sheets from CSV files.
"""

import os
import csv
from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

SCOPES = [
    'https://www.googleapis.com/auth/spreadsheets',
    'https://www.googleapis.com/auth/drive.file'
]


def authenticate():
    """Authenticate with Google API."""
    creds = None
    token_file = 'token.json'

    if os.path.exists(token_file):
        creds = Credentials.from_authorized_user_file(token_file, SCOPES)

    if not creds or not creds.valid:
        print("Error: Invalid credentials")
        return None

    return creds


def create_spreadsheet(title):
    """Create a new Google Sheet."""
    creds = authenticate()
    if not creds:
        return None

    try:
        service = build('sheets', 'v4', credentials=creds)
        spreadsheet = {
            'properties': {
                'title': title
            }
        }
        spreadsheet = service.spreadsheets().create(
            body=spreadsheet,
            fields='spreadsheetId,spreadsheetUrl'
        ).execute()

        return spreadsheet
    except HttpError as error:
        print(f"An error occurred: {error}")
        return None


def populate_sheet_from_csv(spreadsheet_id, csv_file):
    """Populate Google Sheet with data from CSV."""
    creds = authenticate()
    if not creds:
        return False

    try:
        service = build('sheets', 'v4', credentials=creds)

        # Read CSV file
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            values = list(reader)

        # Update the sheet
        body = {
            'values': values
        }

        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body=body
        ).execute()

        print(f"Updated {result.get('updatedCells')} cells")

        # Format header row (bold)
        requests = [{
            'repeatCell': {
                'range': {
                    'sheetId': 0,
                    'startRowIndex': 0,
                    'endRowIndex': 1
                },
                'cell': {
                    'userEnteredFormat': {
                        'backgroundColor': {
                            'red': 0.2,
                            'green': 0.2,
                            'blue': 0.2
                        },
                        'textFormat': {
                            'foregroundColor': {
                                'red': 1.0,
                                'green': 1.0,
                                'blue': 1.0
                            },
                            'fontSize': 10,
                            'bold': True
                        }
                    }
                },
                'fields': 'userEnteredFormat(backgroundColor,textFormat)'
            }
        }, {
            'autoResizeDimensions': {
                'dimensions': {
                    'sheetId': 0,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': 13
                }
            }
        }, {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': 0,
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        }]

        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
        ).execute()

        return True
    except HttpError as error:
        print(f"An error occurred: {error}")
        return False


def main():
    import sys

    if len(sys.argv) != 3:
        print("Usage: python create_google_sheet.py <title> <csv_file>")
        sys.exit(1)

    title = sys.argv[1]
    csv_file = sys.argv[2]

    if not os.path.exists(csv_file):
        print(f"Error: File not found: {csv_file}")
        sys.exit(1)

    print(f"Creating Google Sheet: {title}")
    spreadsheet = create_spreadsheet(title)

    if not spreadsheet:
        print("Failed to create spreadsheet")
        sys.exit(1)

    spreadsheet_id = spreadsheet.get('spreadsheetId')
    spreadsheet_url = spreadsheet.get('spreadsheetUrl')

    print(f"Spreadsheet created: {spreadsheet_url}")
    print(f"Populating with data from {csv_file}...")

    if populate_sheet_from_csv(spreadsheet_id, csv_file):
        print("✅ Google Sheet created and populated successfully!")
        print(f"Open: {spreadsheet_url}")
    else:
        print("❌ Failed to populate spreadsheet")
        sys.exit(1)


if __name__ == '__main__':
    main()
