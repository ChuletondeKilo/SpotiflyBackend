from src.app.infrastructure.db.database import SessionLocal
from datetime import datetime, timezone, timedelta
from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from spotipy import Spotify
from spotipy.oauth2 import SpotifyOAuth
from src.app.domain.spotify.models import UserSession, AccessToken, SpotifyUser
from common import SPOTIFY_CONFIG

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_valid_spotify_client(
    session_id: str = Header(...),
    db: Session = Depends(get_db)
) -> Spotify:
    # --- Step 1: Validate session ---
    session = db.query(UserSession).filter_by(session_id=session_id).first()
    if not session:
        raise HTTPException(status_code=401, detail="Invalid or expired session")

    # --- Step 2: Get token associated with session ---
    token_entry = db.query(AccessToken).filter_by(session_id=session_id).first()
    if not token_entry:
        raise HTTPException(status_code=401, detail="No access token associated with session")

    # --- Step 3: Check token validity ---
    now = datetime.now(timezone.utc)

    expires_at = token_entry.expires_at
    if expires_at.tzinfo is None:
        expires_at = expires_at.replace(tzinfo=timezone.utc)

    if expires_at > now:
        # ✅ Token still valid
        return Spotify(auth=token_entry.access_token)

    # --- Step 4: Token expired: try to refresh it ---
    auth_manager = SpotifyOAuth(**SPOTIFY_CONFIG)
    token_info = {
        "access_token": token_entry.access_token,
        "refresh_token": token_entry.refresh_token,
        "expires_at": int(token_entry.expires_at.timestamp()),
        "token_type": token_entry.token_type,
        "scope": token_entry.scope,
    }

    valid_token = auth_manager.validate_token(token_info)
    if not valid_token:
        raise HTTPException(status_code=403, detail="Token expired and refresh failed")

    # --- Step 5: Update token in DB ---
    if valid_token["access_token"] != token_info["access_token"]:
        token_info["access_token"] = valid_token["access_token"]
        token_info["expires_at"] = datetime.fromtimestamp(valid_token["expires_at"])
        db.commit()

    return Spotify(auth=valid_token["access_token"])