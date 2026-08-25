from google.oauth2.credentials import Credentials
from googleapiclient.discovery import build
from config import BLOG_ID
import os
import base64

if "BLOGGER_TOKEN" in os.environ:
    with open("token.json","wb") as f:
        f.write(base64.b64decode(os.environ["BLOGGER_TOKEN"]))
        
SCOPES=["https://www.googleapis.com/auth/blogger"]

def get_service():

    creds=Credentials.from_authorized_user_file(
        "token.json",
        SCOPES
    )

    return build(
        "blogger",
        "v3",
        credentials=creds
    )

def publish(title,html):

    service=get_service()

    post={
        "title":title,
        "content":html
    }

    result=service.posts().insert(
        blogId=BLOG_ID,
        body=post,
        isDraft=False
    ).execute()

    return result["url"]