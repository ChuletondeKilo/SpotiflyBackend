from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """
    Base schema for Spotify API responses.
    """
    class Config:
        extra = "ignore"

class createPlaylistRequest(BaseSchema):
    """
    Schema for creating a playlist request.
    """
    artist: str = Field(..., description="List of artist IDs")
    playlist_name: str = Field(..., description="Name of the playlist")