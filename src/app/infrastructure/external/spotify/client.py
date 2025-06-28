from spotipy import Spotify
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
from fastapi import HTTPException

class SpotifyClient:
    def __init__(self, client_id: str, client_secret: str, redirect_uri: str = 'http://localhost', scope: str = None):
        """
        Initializes the Spotify client with the necessary credentials.
        """
        self.client_id = client_id
        self.client_secret = client_secret
        self.redirect_uri = redirect_uri
        self.scope = scope
        self.spotify: Spotify = self._create_spotify_instance()

    def _create_spotify_instance(self) -> Spotify:
        """
        Creates a Spotify client instance using Spotipy's SpotifyOAuth.
        """
        try:
            auth_manager = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri="http://127.0.0.1:8888/callback",
            scope="playlist-modify-private playlist-modify-public"
        )
            return Spotify(auth_manager=auth_manager)
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Spotify connection error: {str(e)}")

# a = SpotifyClient(
#     client_id="11bd4dde46104468a7def8ec71918cca",
#     client_secret="06853e4823f6405ca732894cab02ec12",
#     scope='user-library-read playlist-modify-public'
# )

# print(a.spotify.artist_top_tracks('7dGJo4pcD2V6oG8kP0tJRR'))