from pydantic import BaseModel, Field
from datetime import datetime
from ..common import BaseSchema


class ArtistSchema(BaseSchema):
    """
    Schema for Spotify Artist data.
    """
    id: str = Field(..., description="Unique identifier for the artist")
    name: str = Field(..., description="Name of the artist")
    genres: list[str] = Field(default_factory=list, description="Genres associated with the artist")
    images: list[dict] = Field(default_factory=list, description="Images associated with the artist")
    external_urls: dict = Field(default_factory=dict, description="External URLs for the artist")

class SongTrackSchema(BaseSchema):
    """
    Schema for Spotify Track data.
    """
    id: str = Field(..., description="Unique identifier for the track")
    name: str = Field(..., description="Name of the track")
    artists: list[ArtistSchema] = Field(default_factory=list, description="List of artists associated with the track")
    album: dict = Field(default_factory=dict, description="Album information for the track")
    duration_ms: int = Field(..., description="Duration of the track in milliseconds")

class SongCollectionSchema(BaseSchema):
    """
    Schema for a collection of songs.
    """
    items: list[SongTrackSchema] = Field(default_factory=list, description="List of song tracks")
    
    def songs_list(self) -> list[str]:
        """
        Returns a list of song IDs from the collection.
        """
        return [song.id for song in self.items]

class SpotifyUserSchema(BaseModel):
    id: str
    display_name: str | None = None

    class Config:
        orm_mode = True

class UserSessionSchema(BaseModel):
    session_id: str
    user_id: str
    created_at: datetime
    last_active_at: datetime

    class Config:
        orm_mode = True

class AccessTokenSchema(BaseModel):
    session_id: str
    access_token: str
    refresh_token: str | None = None
    token_type: str = "Bearer"
    scope: str | None = None
    expires_at: datetime

    class Config:
        orm_mode = True
