from fastapi import FastAPI, Query, HTTPException
from dotenv import load_dotenv
import os
import tweepy
from typing import List

# Load environment variables.......
load_dotenv("cred.env")

# Initialize FastAPI app
app = FastAPI(title="Twitter API v2 Post Search", version="1.0.0")

# Authenticate with Twitter API v2 using Bearer Token
bearer_token = os.getenv("BEARER_TOKEN")
if not bearer_token:
    raise RuntimeError("Bearer Token is missing. Check your .env file.")

# Initialize Tweepy client
client = tweepy.Client(bearer_token=bearer_token)

@app.get("/")
def root():
    return {"message": "Welcome to Twitter API v2 Search"}

@app.get("/search")
def search_posts(query: str = Query(..., min_length=1), max_results: int = Query(5, ge=1, le=100)) -> List[dict]:
    """
    Search for tweets using Twitter API v2.
    :param query: The search query string.
    :param max_results: The maximum number of tweets to return (default: 10, max: 100).
    :return: A list of tweets matching the query.
    """
    try:
        # Use the client to search for tweets
        response = client.search_recent_tweets(query=query, max_results=max_results)
        if not response.data:
            return []

        # Format the response
        results = []
        for tweet in response.data:
            results.append({
                "id": tweet.id,
                "text": tweet.text,
                "author_id": tweet.author_id,
                "created_at": tweet.created_at if hasattr(tweet, "created_at") else None,
            })
        return results
    except tweepy.TweepyException as e:
        raise HTTPException(status_code=500, detail=f"Error with Twitter API: {e}")
