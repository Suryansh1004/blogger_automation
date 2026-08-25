# AI Blogger Bot

An automated blog publishing service that uses Google Gemini to generate SEO-friendly blog content and publishes it to Google Blogger.

## Features

- Generates unique blog topics with Gemini
- Avoids duplicate topics using SQLite
- Generates long-form Markdown blog content
- Converts Markdown to HTML
- Publishes posts to Google Blogger
- API-key protected publishing endpoint
- Request rate limiting
- Configurable application logging
- Docker deployment support

## Requirements

- Python 3.12+
- Google Gemini API key
- Google Blogger API credentials
- A Google Blogger blog ID

## Installation

```bash
git clone <repository-url>
cd blog_automation

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt