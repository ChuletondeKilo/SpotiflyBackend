from sqlalchemy import Column, String, DateTime, ForeignKey
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from uuid import uuid4
from datetime import datetime, timezone

Base = declarative_base()


class SpotifyUser(Base):
    __tablename__ = "spotify_users"

    id = Column(String, primary_key=True)  # Spotify user ID
    display_name = Column(String)

    # One user -> many sessions
    sessions = relationship("UserSession", back_populates="user", cascade="all, delete-orphan")


class UserSession(Base):
    __tablename__ = "user_sessions"

    session_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    user_id = Column(String, ForeignKey("spotify_users.id", ondelete="CASCADE"))
    created_at = Column(DateTime, default=datetime.now(timezone.utc))
    last_active_at = Column(DateTime, default=datetime.now(timezone.utc))

    # Relationships
    user = relationship("SpotifyUser", back_populates="sessions")
    token = relationship("AccessToken", back_populates="session", uselist=False, cascade="all, delete-orphan")

class AccessToken(Base):
    __tablename__ = "access_tokens"

    token_id = Column(String, primary_key=True, default=lambda: str(uuid4()))
    session_id = Column(String, ForeignKey("user_sessions.session_id", ondelete="CASCADE"))

    access_token = Column(String, nullable=False)
    refresh_token = Column(String)
    token_type = Column(String, default="Bearer")
    scope = Column(String)
    expires_at = Column(DateTime, nullable=False)

    # Back-reference
    session = relationship("UserSession", back_populates="token")

__all__ = [
    "AccessToken",
    "SpotifyUser",
    "UserSession",
    "Base"
]