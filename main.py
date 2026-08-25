from logging_config import configure_logging

configure_logging()

import logging
from fastapi import FastAPI, Request
from slowapi.errors import RateLimitExceeded
from slowapi.extension import _rate_limit_exceeded_handler
from slowapi.middleware import SlowAPIMiddleware
from slowapi.util import get_remote_address
from config import API_SECRET
from database import init_db,topic_exists,save_topic,get_previous_titles
from blog_generator import choose_editorial_format,generate_topic,generate_blog
from blogger_client import publish
from news import fetch_ai_headlines
from fastapi import HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from bootstrap_credentials import create_google_files
from slowapi import Limiter

logger = logging.getLogger(__name__)

limiter=Limiter(key_func=get_remote_address)

create_google_files()

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],   # For local development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)
app.add_middleware(SlowAPIMiddleware)

init_db()

@app.get("/")
def home():
    logger.debug("Health check requested")
    return {"message": "AI Blog Bot Running"}

@app.post("/generate-and-publish")
@limiter.limit("20/hour")
def create_blog(request: Request, x_api_key:str=Header(...)):
    """
    add x_api_key in header in postman as  - 
    x-api-key: <your_api_key>
    """
    if x_api_key!=API_SECRET:
        logger.warning("Unauthorized blog generation request from %s", get_remote_address(request))
        raise HTTPException(401,"Unauthorized")
    try:
        logger.info("Starting blog generation and publishing workflow")
        previous_titles = get_previous_titles()
        headlines = fetch_ai_headlines()
        editorial_format = choose_editorial_format()
        title = generate_topic(previous_titles, headlines, editorial_format)
        if topic_exists(title):
            raise HTTPException(status_code=409, detail="Gemini generated an existing topic")

        html = generate_blog(title, editorial_format)
        url = publish(title, html)
        save_topic(title)
        logger.info("Blog generation and publishing workflow completed")

        return {
            "status": "success",
            "title": title,
            "url": url
        }
    except Exception as e:
        logger.exception("Blog generation and publishing workflow failed")
        raise HTTPException(status_code=500, detail=str(e))

