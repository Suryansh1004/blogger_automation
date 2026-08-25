import os
import json
import logging

logger = logging.getLogger(__name__)

def create_google_files():
    creds = os.getenv("BLOGGER_CREDENTIALS_JSON")
    token = os.getenv("BLOGGER_TOKEN")

    if creds:
        with open("credentials.json", "w") as f:
            json.dump(json.loads(creds), f)
        logger.info("Wrote Blogger credentials file from environment")

    if token:
        with open("token.json", "w") as f:
            json.dump(json.loads(token), f)
        logger.info("Wrote Blogger token file from environment")

    if not creds and not token:
        logger.debug("No Blogger credential environment variables provided")