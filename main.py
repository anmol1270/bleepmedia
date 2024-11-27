from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

# Initialize FastAPI
app = FastAPI()

import json

# Load credentials from a JSON config file
MIRO_ACCESS_TOKEN = "eyJtaXJvLm9yaWdpbiI6ImV1MDEifQ_EbZCWDwBUKBH-JABUIAgPnGTPk4"
MIRO_API_URL = "https://api.miro.com/v2"

class CreateBoardRequest(BaseModel):
    board_name: str
    permissions: str
    description: str = None
    team_id: str

@app.post("/create_board")
def create_board(request: CreateBoardRequest):
    headers = {
        "Authorization": f"Bearer {MIRO_ACCESS_TOKEN}",
        "Content-Type": "application/json"
    }
    payload = {
        "name": request.board_name,
        "sharingPolicy": {"access": request.permissions},
        "description": request.description
    }
    if request.team_id:
        payload["team_id"] = request.team_id

    response = requests.post(f"{MIRO_API_URL}/boards", headers=headers, json=payload)

    if response.status_code == 201:
        return response.json()
    else:
        raise HTTPException(status_code=response.status_code, detail=response.json())
