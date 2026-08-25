from fastapi import FastAPI
from database import init_db,topic_exists,save_topic
from blog_generator import generate_topic,generate_blog
from blogger_client import publish
from fastapi import HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bootstrap_credentials import create_google_files

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

@app.get("/generate-and-publish")
def create_blog():
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

