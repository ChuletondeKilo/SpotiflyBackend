from fastapi import APIRouter, Depends
from .schema import createPlaylistRequest
from .common import get_valid_spotify_client
from spotipy import Spotify
from src.app.infrastructure.external.spotify.operators import ArtistsOperator, PlaylistOperator
from os import getenv

playlist = APIRouter(
    prefix='/v1/playlist', tags=['playlist']
)

@playlist.post("/createPlaylist")
async def createPlaylist(
    create_playlist_request: createPlaylistRequest,
    sp: Spotify = Depends(get_valid_spotify_client)
    ):

    artist = ArtistsOperator(sp, create_playlist_request.artist)

    artistSongs = artist.getSongs()

    playlistOperator = PlaylistOperator(sp, create_playlist_request.playlist_name)

    playlistOperator.create(create_playlist_request.playlist_name, artistSongs.songs_list())

    return "List created successfully"



