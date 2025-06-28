from fastapi import APIRouter, Request
from starlette.datastructures import QueryParams
from fastapi.responses import RedirectResponse
import common
from spotipy import SpotifyOAuth

login = APIRouter(
    prefix='/v1/login', tags=['login']
)

@login.get("/main")
async def initial_login():

    auth_manager = SpotifyOAuth(**common.SPOTIFY_CONFIG)
    auth_url = auth_manager.get_authorize_url()
    return RedirectResponse(auth_url)

@login.get("/callback")
async def callback(request: Request):

    query_params: QueryParams = request.query_params
    authorization_code = query_params.get('code')

    if authorization_code:

        auth_manager = SpotifyOAuth(**common.SPOTIFY_CONFIG)
        access_token = auth_manager.get_access_token(authorization_code)


    return RedirectResponse()