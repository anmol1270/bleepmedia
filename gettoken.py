from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
import os
import json

SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CREDS_FILE = 'client_secret_1092296767845-q84049m8pvh9bd12k0n6ta0ft3e1t01c.apps.googleusercontent.com (1).json'
TOKEN_FILE = 'token.json'

def authenticate():
    creds = None
    # Load token if it exists
    if os.path.exists(TOKEN_FILE):
        with open(TOKEN_FILE, 'r') as token:
            creds = json.load(token)

    # If no valid credentials, run the OAuth flow
    if not creds or not creds.get('refresh_token'):
        flow = InstalledAppFlow.from_client_secrets_file(CREDS_FILE, SCOPES)
        creds = flow.run_local_server(port=5000)  # Match the Uvicorn server port
        # Save the credentials for the next run
        with open(TOKEN_FILE, 'w') as token:
            token.write(creds.to_json())

    return creds

if __name__ == "__main__":
    authenticate()
