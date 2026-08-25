from dotenv import load_dotenv
import os

load_dotenv()

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
BLOG_ID=os.getenv("BLOG_ID")