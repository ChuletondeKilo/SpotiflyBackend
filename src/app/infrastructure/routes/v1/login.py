from fastapi import APIRouter
from fastapi.responses import RedirectResponse
from spotipy.oauth2 import SpotifyOAuth
from spotipy import Spotify
from os import getenv

login = APIRouter(
    prefix='/v1/login', tags=['login']
)

@login.get("/main")
def initial_login():
    auth_manager = SpotifyOAuth(
            client_id=getenv("CLIENT_ID"),
            client_secret=getenv("CLIENT_SECRET"),
            redirect_uri="https://localhost:8000",
            scope="playlist-modify-private playlist-modify-public user-library-read"
        )
    auth_url = auth_manager.get_authorize_url()
    return RedirectResponse(auth_url)

@login.get("/callback")
def callback(code: str):
    auth_manager = SpotifyOAuth(
            client_id=getenv("CLIENT_ID"),
            client_secret=getenv("CLIENT_SECRET"),
            redirect_uri="http://127.0.0.1:8888/v1/login/callback",
            scope="playlist-modify-private playlist-modify-public user-library-read"
        )
    token_info = auth_manager.get_access_token(code)
    access_token = token_info["access_token"]
    refresh_token = token_info["refresh_token"] 
    
    # Store this in session/db for user
    sp = Spotify(auth=access_token)
    user = sp.current_user()

    return {"message": f"Logged in as {user['display_name']}", "token": access_token}