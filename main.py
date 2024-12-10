from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from twilio.rest import Client
from dotenv import load_dotenv
import os

load_dotenv(dotenv_path='cred.env')

app = FastAPI()

# Load Twilio credentials from environment variables
account_sid = os.getenv('TWILIO_ACCOUNT_SID')
auth_token = os.getenv('TWILIO_AUTH_TOKEN')
client = Client(account_sid, auth_token)

class PhoneNumberRequest(BaseModel):
    country: str
    area_code: str = None

@app.post("/buy-number/")
async def buy_number(request: PhoneNumberRequest):
    try:
        # Search for available phone numbers
        numbers = client.available_phone_numbers(request.country).local.list(
            area_code=request.area_code, sms_enabled=True, limit=1
        )
        if not numbers:
            raise HTTPException(status_code=404, detail="No available phone numbers found.")

        # Purchase the first available number
        purchased_number = client.incoming_phone_numbers.create(phone_number=numbers[0].phone_number)
        return {"purchased_number": purchased_number.phone_number}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
