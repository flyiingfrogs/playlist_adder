import requests
import json
import dotenv
import os

dotenv.load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = "http://127.0.0.1:8888/callback"

def get_token():
    url = "https://accounts.spotify.com/api/token"
    headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }
    data = {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret
    }

    response = requests.post(url, headers=headers, data=data)
    if response.status_code == 200:
        token_info = response.json()
        return token_info["access_token"]

