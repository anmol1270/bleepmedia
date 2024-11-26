from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import requests

# Initialize FastAPI
app = FastAPI()

import json

# Load credentials from a JSON config file
with open("config.json") as config_file:
    config = json.load(config_file)

WORDPRESS_BASE_URL = config["WORDPRESS_BASE_URL"]
WORDPRESS_USERNAME = config["WORDPRESS_USERNAME"]
WORDPRESS_PASSWORD = config["WORDPRESS_PASSWORD"]
# Pydantic model for request validation
class BlogPost(BaseModel):
    title: str
    content: str
    categories: list[str] = []
    tags: list[str] = []
    featured_image: str = None
    status: str = "publish"
    author: str = None

# Helper function to create or get taxonomy ID
def get_or_create_taxonomy_id(base_url, taxonomy, name, auth):
    taxonomy_url = f"{base_url}/wp-json/wp/v2/{taxonomy}"
    response = requests.get(taxonomy_url, auth=auth)
    items = response.json()

    for item in items:
        if item["name"].lower() == name.lower():
            return item["id"]

    # Create the taxonomy if not found
    response = requests.post(taxonomy_url, json={"name": name}, auth=auth)
    print(response)
    return response.json()["id"]

# Helper function to upload featured image
def upload_featured_image(base_url, image_url, auth):
    upload_url = f"{base_url}/wp-json/wp/v2/media"
    headers = {"Content-Disposition": f"attachment; filename={image_url.split('/')[-1]}"}

    # Download the image
    image_response = requests.get(image_url)
    if image_response.status_code != 200:
        raise HTTPException(status_code=400, detail="Failed to download the image.")

    # Upload the image
    response = requests.post(upload_url, headers=headers, data=image_response.content, auth=auth)
    if response.status_code == 201:
        return response.json()["id"]
    else:
        raise HTTPException(status_code=400, detail=f"Failed to upload image: {response.json()}")

# FastAPI route to handle WordPress post creation
@app.post("/publish_wordpress_post")
def publish_wordpress_post(post: BlogPost):
    auth = (WORDPRESS_USERNAME, WORDPRESS_PASSWORD)
    api_endpoint = f"{WORDPRESS_BASE_URL}/wp-json/wp/v2/posts"

    # Prepare the payload
    payload = {
        "title": post.title,
        "content": post.content,
        "status": post.status
    }

    if post.author:
        payload["author"] = post.author

    # Add categories and tags by name or create them
    payload["categories"] = [
        get_or_create_taxonomy_id(WORDPRESS_BASE_URL, "categories", cat, auth)
        for cat in post.categories
    ]
    payload["tags"] = [
        get_or_create_taxonomy_id(WORDPRESS_BASE_URL, "tags", tag, auth)
        for tag in post.tags
    ]

    # Handle featured image
    if post.featured_image:
        payload["featured_media"] = upload_featured_image(WORDPRESS_BASE_URL, post.featured_image, auth)

    # Publish the post
    response = requests.post(api_endpoint, json=payload, auth=auth)
    if response.status_code == 201:
        return {"message": "Post published successfully", "data": response.json()}
    else:
        raise HTTPException(status_code=400, detail=f"Failed to publish post: {response.json()}")
