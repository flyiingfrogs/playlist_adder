import requests
import urllib.parse
import dotenv
import os
import threading
import webbrowser
import json
from callback_server import AuthCodeCatcher


dotenv.load_dotenv()

client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
redirect_uri = "http://127.0.0.1:8888/callback"
scope = "user-read-currently-playing user-read-playback-state playlist-modify-public"

headers = {
        'Content-Type': 'application/x-www-form-urlencoded'
    }

token_url = "https://accounts.spotify.com/api/token"

def get_auth_url():
    base_url = "https://accounts.spotify.com/authorize"
    params = {
        "client_id": client_id,
        "response_type": "code",
        "redirect_uri": redirect_uri,
        "scope": scope,
        "show_dialog": "true"
    }
    url = base_url + "?" + urllib.parse.urlencode(params)
    return url
    
def exchange_code_for_token(code):
    data = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": redirect_uri,
    }
    auth = requests.auth.HTTPBasicAuth(client_id, client_secret)
    response = requests.post(token_url, data=data, auth=auth)
    response.raise_for_status()
    return response.json()


def authorize_user():
    catcher = AuthCodeCatcher()
    server_thread = threading.Thread(target=catcher.run_once)
    server_thread.start()

    auth_url = get_auth_url()
    webbrowser.open(auth_url)
    print("Authorize spotify here: ", auth_url)

    server_thread.join()

    if catcher.auth_code:
        print("Authorization code received: ", catcher.auth_code)
        tokens = exchange_code_for_token(catcher.auth_code)
        server_thread.join()
        return [catcher.auth_code, tokens.get("refresh_token"), tokens["access_token"]]

def get_curr_track(token):
    url = "https://api.spotify.com/v1/me/player/currently-playing"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    response = requests.get(url, headers=headers)

    if response.status_code == 200: 
        data = json.loads(response.text)
        print(data['item']['name'])
        return data['item']['uri']


def playlist_exists():
    pass    

def create_playlist(playlistName, token):
    url = "https://api.spotify.com/v1/me/playlists"
    headers = {
        'Authorization': f'Bearer {token}'
    }
    data = {
        "name": f"{playlistName}"
    }
    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("playlist created successfully")
        data = json.loads(response.text)
        return data['uri']

def add_track(track, playlist, token):

    pid = playlist.split(':')[2]
    url = f"https://api.spotify.com/v1/playlists/{pid}/items"
    headers = {
        'Authorization': f'Bearer {token}',
        'Content-Type': 'application/json'
    }

    data = {
        "uris": [track],
        "position": 0
    }

    response = requests.post(url, headers=headers, json=data)

    if response.status_code == 201:
        print("track added successfully")
        return response.json

# [auth_code, refresh_token, access_token] = authorize_user()
# track_id = get_curr_track(access_token)
# playlist_id = create_playlist("test",access_token)
# add_track(track_id, playlist_id, access_token)

