from fastapi import FastAPI
from slowapi.util import get_remote_address
from config import API_SECRET
from database import init_db,topic_exists,save_topic
from blog_generator import generate_topic,generate_blog
from blogger_client import publish
from fastapi import HTTPException, Header
from fastapi.middleware.cors import CORSMiddleware
from bootstrap_credentials import create_google_files
from slowapi import Limiter

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

init_db()

@app.get("/")
def home():
    return {"message": "AI Blog Bot Running"}

@app.post("/generate-and-publish")
@limiter.limit("20/hour")
def create_blog(x_api_key:str=Header(...)):
    if x_api_key!=API_SECRET:
        raise HTTPException(401,"Unauthorized")
    try:
        while True:
            title = generate_topic()
            if not topic_exists(title):
                break

        html = generate_blog(title)
        url = publish(title, html)
        save_topic(title)

        return {
            "status": "success",
            "title": title,
            "url": url
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

