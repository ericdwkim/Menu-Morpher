import os.path
from google.auth.transport.requests import Request
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow

# Define the scopes
SCOPES = ['https://www.googleapis.com/auth/business.manage']

# Function to get credentials
def get_credentials():
    creds = None
    if os.path.exists('../token.json'):
        creds = Credentials.from_authorized_user_file('../token.json', SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            # TODO: relative json file paths for both creds and token
            flow = InstalledAppFlow.from_client_secrets_file(
                '/Users/ekim/workspace/personal/menu-morpher/utils/credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
        with open('../token.json', 'w') as token:
            token.write(creds.to_json())
    return creds

def get_account_id():

    # Initialize the Google My Business API
    creds = get_credentials()
    service_mbam = build('mybusinessaccountmanagement', 'v1', credentials=creds)

    # List all accounts
    accounts = service_mbam.accounts().list().execute()
    for account in accounts.get('accounts', []):
        account_id = account['name']
        return account_id


# TODO: turn service into importable object for main app script to be used for `getCanHaveFoodMenus()` helper function
def get_account_and_location_ids():

    # Initialize the Google My Business API
    creds = get_credentials()

    account_id = get_account_id()

    service_mbbi = build('mybusinessbusinessinformation', 'v1', credentials=creds)
    # List locations for each account
    locations = service_mbbi.accounts().locations().list(
        parent=account_id,
        readMask='name'
    ).execute()

    location_id = locations['locations'][0]['name']
    # print(account_id, location_id)
    return account_id, location_id



