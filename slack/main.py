from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

SLACK = "xoxb-8102575069952-8085946403206-YQh6xsJGiSEukTIlZZCoGsej"

app = FastAPI()

class ChannelDetails(BaseModel):
    name: str
    description: str
    is_private: bool

@app.post("/create_channel/")
def create_channel(details: ChannelDetails):
    headers = {"Authorization": f"Bearer {SLACK}"}
    url = "https://slack.com/api/conversations.create"

    payload = {
        "name": details.name,
        "is_private": details.is_private
    }

    # Create the channel
    response = requests.post(url, headers=headers, json=payload)
    data = response.json()

    if not data.get("ok"):
        raise HTTPException(status_code=400, detail=data.get("error"))

    # Set the channel topic/description
    topic_url = "https://slack.com/api/conversations.setTopic"
    topic_payload = {
        "channel": data["channel"]["id"],
        "topic": details.description
    }

    requests.post(topic_url, headers=headers, json=topic_payload)

    return {"channel_id": data["channel"]["id"], "channel_name": details.name}
