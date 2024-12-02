from fastapi import FastAPI, HTTPException, Query,Depends
import requests
from pydantic import BaseModel
import xmltodict


app = FastAPI(
    title="USPTO Trademark Assignment Search API",
    description="Backend for searching trademark assignments using USPTO Assignment API.",
    version="1.0.0"
)

USPTO_API_BASE_URL = "https://assignment-api.uspto.gov/trademark/lookup"

class Params(BaseModel):
    query: str  # Required search term
    filter: str  # Required filter value
    accept: str = "application/xml"

@app.get("/trademark/v1/quickLookup")
async def search_trademarks(params: Params = Depends()):
    """
    Search trademarks using the USPTO API.
    """
    try:

        headers = {
            "Accept": "application/xml"
        }
        # Construct request parameters
        params = {
            "query": params.query,
            "filter": params.filter,
            "rows":"5",
            
            
        }

        # Make the API call to USPTO
        response = requests.get(USPTO_API_BASE_URL, headers=headers,params=params)
        response.raise_for_status()  # Raise an error for bad status codes
        json_data = xmltodict.parse(response.text)

        # Return the JSON response
        return json_data

    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Error connecting to USPTO API: {str(e)}")

@app.get("/")
async def root():
    return {"message": "Welcome to the USPTO Trademark Assignment Search API backend."}
