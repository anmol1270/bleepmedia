

## Overview

This project provides a Python-based REST API built using FastAPI that allows you to publish blog posts to a WordPress site programmatically. The API handles post creation, category and tag management, and uploading featured images. It's a simple and effective solution to automate WordPress blog publishing.

---

## Features

- Create and publish blog posts to WordPress.
- Automatically create or retrieve WordPress categories and tags.
- Upload featured images for blog posts.
- Authenticate with WordPress using credentials.
- Flexible and customizable payloads with fields for title, content, categories, tags, and more.

---

## Prerequisites

- **Python**: Make sure you have Python 3.8 or later installed.
- **FastAPI**: The application is built using FastAPI.
- **WordPress REST API**: Ensure the WordPress site has REST API enabled.
- **Authentication**: WordPress username and application-specific password or OAuth token.

---

## Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/your-username/wordpress-blog-publisher.git
   cd wordpress-blog-publisher
   ```

2. Install required Python dependencies:
   ```bash
   pip install fastapi uvicorn pydantic requests
   ```

3. Configure your WordPress credentials in the `main.py` file:
   ```python
   WORDPRESS_BASE_URL = "https://your-wordpress-site.com"
   WORDPRESS_USERNAME = "your-username"
   WORDPRESS_PASSWORD = "your-application-password"
   ```

---

## Usage

1. Start the FastAPI server:
   ```bash
   uvicorn main:app --reload
   ```

2. Use the `/publish_wordpress_post` endpoint to create and publish a WordPress blog post.

   Example request payload:
   ```json
   {
       "title": "My First Blog Post",
       "content": "This is the content of the blog post.",
       "categories": ["Technology", "Python"],
       "tags": ["FastAPI", "Automation"],
       "featured_image": "https://example.com/image.jpg",
       "status": "publish",
       "author": "1"
   }
   ```

3. Send a POST request to the endpoint:
   ```bash
   curl -X POST "http://127.0.0.1:8000/publish_wordpress_post" \
   -H "Content-Type: application/json" \
   -d '{
       "title": "My First Blog Post",
       "content": "This is the content of the blog post.",
       "categories": ["Technology", "Python"],
       "tags": ["FastAPI", "Automation"],
       "featured_image": "https://example.com/image.jpg",
       "status": "publish"
   }'
   ```

---

## Endpoints

### `/publish_wordpress_post`

- **Method**: `POST`
- **Description**: Creates and publishes a blog post to WordPress.
- **Request Body**:
  - `title` (string): The title of the blog post.
  - `content` (string): The main content of the blog post.
  - `categories` (list of strings): List of categories to associate with the post.
  - `tags` (list of strings): List of tags for the post.
  - `featured_image` (string, optional): URL of the featured image.
  - `status` (string, optional): Post status (`draft`, `publish`). Default is `publish`.
  - `author` (string, optional): The WordPress user ID of the author.
- **Response**:
  - Success: JSON object with a success message and post details.
  - Failure: HTTP 400 with an error message.

---

## Security

- Ensure your WordPress credentials are stored securely and not hardcoded in the source code.
- Use environment variables or a secure secrets manager for sensitive information.

---

## Contributions

Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.

---

## License

This project is licensed under the MIT License. See the `LICENSE` file for more details.

---

## Contact

For any issues or feature requests, feel free to contact the repository owner or open an issue on GitHub.
