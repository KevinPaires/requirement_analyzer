#!/usr/bin/env python3
"""
Update existing Google Sheet with new CSV data
"""

import os
import csv
import sys
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
import pickle

SCOPES = ['https://www.googleapis.com/auth/spreadsheets']

def authenticate():
    """Authenticate with Google Sheets API"""
    creds = None
    if os.path.exists('token.pickle'):
        with open('token.pickle', 'rb') as token:
            creds = pickle.load(token)

    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file(
                'credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)

        with open('token.pickle', 'wb') as token:
            pickle.dump(creds, token)

    return build('sheets', 'v4', credentials=creds)

def clear_sheet(service, spreadsheet_id):
    """Clear all content from Sheet1"""
    try:
        # Get the sheet properties to find the sheet ID
        spreadsheet = service.spreadsheets().get(spreadsheetId=spreadsheet_id).execute()
        sheet_id = spreadsheet['sheets'][0]['properties']['sheetId']

        # Clear all content
        service.spreadsheets().values().clear(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A1:Z10000'
        ).execute()

        print("✓ Sheet content cleared")
        return sheet_id
    except Exception as e:
        print(f"Error clearing sheet: {e}")
        return None

def populate_sheet_from_csv(service, spreadsheet_id, csv_file):
    """Populate sheet with CSV data"""
    try:
        # Read CSV file
        with open(csv_file, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            values = list(reader)

        # Update the sheet
        result = service.spreadsheets().values().update(
            spreadsheetId=spreadsheet_id,
            range='Sheet1!A1',
            valueInputOption='RAW',
            body={'values': values}
        ).execute()

        print(f"✓ Updated {result.get('updatedCells')} cells")
        return True
    except Exception as e:
        print(f"Error populating sheet: {e}")
        return False

def format_sheet(service, spreadsheet_id, sheet_id, num_rows):
    """Apply formatting to the sheet"""
    requests = [
        # Format header row (bold, dark background, white text)
        {
            'repeatCell': {
                'range': {
                    'sheetId': sheet_id,
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
        },
        # Freeze header row
        {
            'updateSheetProperties': {
                'properties': {
                    'sheetId': sheet_id,
                    'gridProperties': {
                        'frozenRowCount': 1
                    }
                },
                'fields': 'gridProperties.frozenRowCount'
            }
        },
        # Auto-resize all columns
        {
            'autoResizeDimensions': {
                'dimensions': {
                    'sheetId': sheet_id,
                    'dimension': 'COLUMNS',
                    'startIndex': 0,
                    'endIndex': 13
                }
            }
        }
    ]

    try:
        service.spreadsheets().batchUpdate(
            spreadsheetId=spreadsheet_id,
            body={'requests': requests}
        ).execute()
        print("✓ Formatting applied")
        return True
    except Exception as e:
        print(f"Error formatting sheet: {e}")
        return False

def main():
    if len(sys.argv) != 3:
        print("Usage: python update_google_sheet.py <spreadsheet_id> <csv_file>")
        sys.exit(1)

    spreadsheet_id = sys.argv[1]
    csv_file = sys.argv[2]

    if not os.path.exists(csv_file):
        print(f"Error: CSV file not found: {csv_file}")
        sys.exit(1)

    print(f"Updating Google Sheet: {spreadsheet_id}")

    # Authenticate
    service = authenticate()

    # Clear existing content
    sheet_id = clear_sheet(service, spreadsheet_id)
    if sheet_id is None:
        sys.exit(1)

    # Populate with new CSV data
    if not populate_sheet_from_csv(service, spreadsheet_id, csv_file):
        sys.exit(1)

    # Count rows for formatting
    with open(csv_file, 'r', encoding='utf-8') as f:
        num_rows = sum(1 for _ in f)

    # Apply formatting
    if not format_sheet(service, spreadsheet_id, sheet_id, num_rows):
        sys.exit(1)

    print(f"\n✅ Successfully updated spreadsheet!")
    print(f"🔗 Open: https://docs.google.com/spreadsheets/d/{spreadsheet_id}/edit")

if __name__ == '__main__':
    main()
