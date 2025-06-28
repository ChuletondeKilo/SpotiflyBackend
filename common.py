from uuid import uuid4
from os import getenv
from dotenv import load_dotenv

load_dotenv()

state = uuid4()
SPOTIFY_CONFIG = {
    "client_id": getenv("CLIENT_ID"),
    "client_secret": getenv("CLIENT_SECRET"),
    "redirect_uri": "http://localhost:8000/v1/login/callback",
    "scope": "playlist-modify-private playlist-modify-public user-library-read",
    "state": state
}
