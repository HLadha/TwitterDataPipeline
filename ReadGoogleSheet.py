import os.path
import gspread
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SPREADSHEET_ID = ""

def getCredentials():
    flow = InstalledAppFlow.from_client_secrets_file(
        'sheetsCred.json', SCOPES)

    creds = flow.run_local_server(port=0)
    with open('token.json', 'w') as token:
        token.write(creds.to_json())

    return creds

def getSheetData():
    creds = None
    # The file sheetsCred contains the access token and refresh token, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('sheetsCred.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception('No valid credentials found')

    client = gspread.authorize(creds)

    # Open the Google Spreadsheet by its ID
    sheet = client.open_by_key(SPREADSHEET_ID)

    # Get all records of the data
    data = sheet.worksheet("Twitter Scrapper Config").get_all_records()
    return data

def getRidingSheetData():
    creds = None
    # The file sheetsCred contains the access token and refresh token, and is
    # created automatically when the authorization flow completes for the first time.
    if os.path.exists('sheetsCred.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    # If there are no (valid) credentials available, prompt the user to log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception('No valid credentials found')

    client = gspread.authorize(creds)

    # Open the Google Spreadsheet by its ID
    sheet = client.open_by_key(SPREADSHEET_ID)

    # Get all records of the data
    data = sheet.worksheet("Backend Pls Don't Touch").get_all_records()
    return data

def writeIDToSheet(twitter_handle, id):
    creds = None
    if os.path.exists('sheetsCred.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception('No valid credentials found')

    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.worksheet("Twitter Scrapper Config")

    twitter_handles = worksheet.col_values(3)  # Assuming Twitter handles are in column 2
    row = twitter_handles.index(twitter_handle) + 1  # Add 1 because gspread rows start at 1

    worksheet.update_cell(row, 4, id)  # Assuming IDs should be written to column 3

def writeCaptureStatus(name, status):
    creds = None
    if os.path.exists('sheetsCred.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception('No valid credentials found')

    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.worksheet("Twitter Scrapper Config")

    names = worksheet.col_values(1)  # Assuming Twitter handles are in column 2
    row = names.index(name) + 1  # Add 1 because gspread rows start at 1

    worksheet.update_cell(row, 6, status)  # Assuming status should be written to column 4

def write_toSheet(data):
    creds = None
    if os.path.exists('sheetsCred.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            raise Exception('No valid credentials found')

    client = gspread.authorize(creds)
    sheet = client.open_by_key(SPREADSHEET_ID)
    worksheet = sheet.worksheet("Data Review (API Capture)")

    # Write the headings
    headings = ["Riding Code", "Name", "Handle", "ID", "URL", "Tweet", "Time"]
    data.insert(0, headings)

    # Write all the data in bulk
    worksheet.append_rows(data)
