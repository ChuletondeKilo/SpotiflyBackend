from fastapi import APIRouter, Header, HTTPException
from .schema import createPlaylistRequest
from spotipy import Spotify
from src.app.infrastructure.external.spotify.operators import ArtistsOperator, PlaylistOperator
from src.app.infrastructure.external.spotify.client import SpotifyClient
from os import getenv

playlist = APIRouter(
    prefix='/v1/playlist', tags=['playlist']
)

@playlist.post("/createPlaylist")
async def createPlaylist(
    create_playlist_request: createPlaylistRequest
    ):

    # if not authorization.startswith("Bearer "):
    #     raise HTTPException(status_code=401, detail="Invalid token format")

    # access_token = authorization.removeprefix("Bearer ").strip()

    sp = Spotify(auth="""BQCXa44J6My1QHcNHq5trs1OrkeC0MA4t7HDcfgdwzb-R4mQUyXTSnHq9c7ni3-9cnMccPOGgxxWhOew8w5jGOOJQX35nYhuJUowYTE8SRpsLULtHx_YXpGGZR2_CZ1x_AxV48kzTRV7pw5yezHn0VyUJJxz5YV79U1Y1Mp17rv_0fy9_xpXhSpXPufVtyhAXvtWV1TrNQsuOWjjgdM5M7xOHjkqdCxCN4fFlOU_N3sIjMPso99Z1s9q92YtGLR2rbjmKmdxA7L7Eddt""")

    artist = ArtistsOperator(sp, create_playlist_request.artist)

    artistSongs = artist.getSongs()

    playlistOperator = PlaylistOperator(sp, create_playlist_request.playlist_name)

    playlistOperator.create(create_playlist_request.playlist_name, artistSongs.songs_list())

    return "List created successfully"



