from google_auth_oauthlib.flow import InstalledAppFlow
import os

os.environ['OAUTHLIB_INSECURE_TRANSPORT'] = '1'
print("OAUTHLIB_INSECURE_TRANSPORT =", os.environ.get('OAUTHLIB_INSECURE_TRANSPORT'))



SCOPES = ["https://www.googleapis.com/auth/admin.directory.group"]
CREDENTIALS_FILE = "creds1.json"

flow = InstalledAppFlow.from_client_secrets_file(CREDENTIALS_FILE, SCOPES,redirect_uri="https://10a8-223-190-85-232.ngrok-free.app/oauth2callback"
)
authorization_url, state = flow.authorization_url(
    access_type="offline", include_granted_scopes="true"
)

print("Visit this URL to authorize:", authorization_url)
