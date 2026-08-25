from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
BLOG_ID=os.getenv("BLOG_ID")
API_SECRET=os.getenv("API_SECRET")