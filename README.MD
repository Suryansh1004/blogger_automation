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
- LangSmith API key and prompt names (optional local fallbacks are used when names are not set)
- Google Blogger API credentials
- A Google Blogger blog ID

## Installation

```bash
git clone <repository-url>
cd blog_automation

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt

Set these environment variables to use prompts managed in LangSmith:

```dotenv
LANGSMITH_TOPIC_PROMPT=your-topic-prompt-name
LANGSMITH_BLOG_PROMPT=your-blog-prompt-name
```

The application accepts `LANGSMITH_API_KEY`, `LANGCHAIN_API_KEY`, or the existing
lowercase `langsmith_api_key` variable. LangSmith tracing is enabled by default;
set `LANGSMITH_TRACING=false` to disable it.