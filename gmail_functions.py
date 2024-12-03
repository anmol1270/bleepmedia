from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
import base64
from email import message_from_bytes
import os

# Load credentials from `credentials.json`
SCOPES = ['https://www.googleapis.com/auth/gmail.modify']
CREDS_FILE = "token.json"

def authenticate_gmail():
    creds = Credentials.from_authorized_user_file(CREDS_FILE, SCOPES)
    return build('gmail', 'v1', credentials=creds)

def decode_email_body(encoded_body):
    """Decodes the email body from base64."""
    decoded_bytes = base64.urlsafe_b64decode(encoded_body)
    return decoded_bytes.decode("utf-8", errors="ignore")

def search_gmail(query: str, max_results: int = 5):
   
    """Search Gmail and fetch metadata."""
    service = authenticate_gmail()
    try:
        results = service.users().messages().list(userId='me', q=query, maxResults=max_results).execute()
        messages = results.get('messages', [])
        email_data = []

        for message in messages:
            msg = service.users().messages().get(userId='me', id=message['id'], format='metadata').execute()
            headers = {header['name']: header['value'] for header in msg['payload']['headers']}
            snippet = msg.get('snippet', '')  # Email snippet only
            email_data.append({
                "id": message['id'],
                "from": headers.get("From", ""),
                "to": headers.get("To", ""),
                "subject": headers.get("Subject", ""),
                "snippet": snippet
            })
        return email_data
    except Exception as e:
        print(f"Error during Gmail API request: {e}")
        raise

from email.mime.text import MIMEText
import base64

def create_reply_email(to_email, subject, message_body, thread_id):
    """Create a MIME email message for replying."""
    message = MIMEText(message_body)
    message['to'] = to_email
    message['subject'] = f"Re: {subject}"  # Prefix "Re:" to indicate a reply
    message['In-Reply-To'] = thread_id
    message['References'] = thread_id
    return {'raw': base64.urlsafe_b64encode(message.as_bytes()).decode()}

def send_email_reply(service, reply_message):
    """Send the email reply using the Gmail API."""
    try:
        message = service.users().messages().send(userId='me', body=reply_message).execute()
        return message
    except Exception as e:
        print(f"Error sending email: {e}")
        raise

