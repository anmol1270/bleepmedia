from fastapi import FastAPI, HTTPException
from gmail_functions import *
from pydantic import BaseModel


app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to Gmail Search GPT Backend"}

@app.get("/search/")
def search_emails(query: str, max_results: int = 5):
    try:
        # Search Gmail
        emails = search_gmail(query, max_results)
        if not emails:
            return {"message": "No emails found."}
        
        return {"emails": emails}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class ReplyEmailRequest(BaseModel):
    email_id: str
    message_body: str

@app.post("/reply/")
def reply_to_email(reply_request: ReplyEmailRequest):
    """Reply to a specific email."""
    try:
        service = authenticate_gmail()
        
        # Fetch the original email details
        email = service.users().messages().get(userId='me', id=reply_request.email_id, format='metadata').execute()
        headers = {header['name']: header['value'] for header in email['payload']['headers']}
        
        # Extract necessary fields
        to_email = headers.get('From')  # Reply to the sender
        subject = headers.get('Subject', "No Subject")
        thread_id = email.get('threadId')

        # Create reply message
        reply_message = create_reply_email(
            to_email=to_email,
            subject=subject,
            message_body=reply_request.message_body,
            thread_id=thread_id
        )
        
        # Send the email
        response = send_email_reply(service, reply_message)
        return {"message": "Reply sent successfully", "response": response}
    
    except Exception as e:
        print(f"Error replying to email: {e}")
        raise HTTPException(status_code=500, detail="Failed to send email reply")