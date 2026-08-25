from dotenv import load_dotenv
import os
import logging

load_dotenv()

logger = logging.getLogger(__name__)

GEMINI_API_KEY=os.getenv("GEMINI_API_KEY")
GEMINI_MODEL = os.getenv("GEMINI_MODEL")
BLOG_ID=os.getenv("BLOG_ID")
API_SECRET=os.getenv("API_SECRET")

logger.info("Configuration loaded for model=%s blog_configured=%s", GEMINI_MODEL, bool(BLOG_ID))