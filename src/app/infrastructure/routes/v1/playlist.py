from fastapi import APIRouter
from .schema import createPlaylistRequest
from spotipy import Spotify
from src.app.infrastructure.external.spotify.operators import ArtistsOperator, PlaylistOperator
from os import getenv

playlist = APIRouter(
    prefix='/v1/playlist', tags=['playlist']
)

@playlist.post("/createPlaylist")
async def createPlaylist(
    create_playlist_request: createPlaylistRequest,
    
    ):

    # if not authorization.startswith("Bearer "):
    #     raise HTTPException(status_code=401, detail="Invalid token format")

    # access_token = authorization.removeprefix("Bearer ").strip()

    sp = Spotify(auth="""AQAyVGnR8-2M-r1vXVm1oInlNrc8kQ1V2kfLjcl9hJmfIusaBU5eTIYUJ7rsvtAClrrm5Tyzmfigh4hR_2jLhoIDeV9zTklxJU81ki3hbL8vYZYpMUMbUXeU6rr9x4K6aELJqfwtXjNlefdV3I-GaEkRM9V02Z7l8wHHZau3GP9rG5zX7Ui36UfaP8QKUzIMVtNsIHdfV1zUXqYpsuZ4RVHbsk65N0xPXagis6B5v9hNqbsSvl9V5V1ft__2N0HVxpdKGCHGrWfwOA2FTaxz""")

    artist = ArtistsOperator(sp, create_playlist_request.artist)

    artistSongs = artist.getSongs()

    playlistOperator = PlaylistOperator(sp, create_playlist_request.playlist_name)

    playlistOperator.create(create_playlist_request.playlist_name, artistSongs.songs_list())

    return "List created successfully"



