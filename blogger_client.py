from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import BLOG_ID
import os
import base64
import logging

logger = logging.getLogger(__name__)
SCOPES=["https://www.googleapis.com/auth/blogger"]

def get_service():
    logger.debug("Loading Blogger authorization")
    creds=Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )

    service = build(
        "blogger",
        "v3",
        credentials=creds
    )
    logger.debug("Blogger service initialized")
    return service

def publish(title,html):
    logger.info("Publishing blog post")
    service=get_service()

    post={
        "title":title,
        "content":html
    }

    try:
        result=service.posts().insert(
            blogId=BLOG_ID,
            body=post,
            isDraft=False
        ).execute()
    except Exception:
        logger.exception("Blogger publish failed")
        raise

    logger.info("Blog post published successfully")
    return result["url"]