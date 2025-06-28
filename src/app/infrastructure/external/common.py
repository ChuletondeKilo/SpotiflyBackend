from pydantic import BaseModel, Field


class BaseSchema(BaseModel):
    """
    Base schema for Spotify API responses.
    """
    class Config:
        extra = "ignore"