from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# FastAPI app initialization
app = FastAPI()

# Service Account and Scopes
SERVICE_ACCOUNT_FILE = "second-petal-444206-n7-e2e9cd9f57b5.json"  # Replace with your file
SCOPES = ["https://www.googleapis.com/auth/admin.directory.group"]
DELEGATED_ADMIN = "founder@praudyogic.com"  # Replace with your super admin email

# Define Pydantic model for input validation
class GroupDetails(BaseModel):
    name: str
    email: str
    description: str

# Function to authenticate and build the Admin SDK service
def get_admin_service():
    credentials = service_account.Credentials.from_service_account_file(
        SERVICE_ACCOUNT_FILE, scopes=SCOPES
    ).with_subject(DELEGATED_ADMIN)

    service = build("admin", "directory_v1", credentials=credentials)
    return service

@app.post("/create-group")
async def create_group(group: GroupDetails):
    """
    Endpoint to create a Google Group.
    """
    try:
        service = get_admin_service()
        group_body = {
            "name": group.name,
            "email": group.email,
            "description": group.description,
        }
        result = service.groups().insert(body=group_body).execute()
        return {"message": "Group created successfully", "group": result}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to create group: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
