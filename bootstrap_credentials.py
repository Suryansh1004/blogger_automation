import os
import json

def create_google_files():

    creds = os.getenv("BLOGGER_CREDENTIALS_JSON")
    token = os.getenv("BLOGGER_TOKEN_JSON")

    if creds:
        with open("credentials.json", "w") as f:
            json.dump(json.loads(creds), f)

    if token:
        with open("token.json", "w") as f:
            json.dump(json.loads(token), f)