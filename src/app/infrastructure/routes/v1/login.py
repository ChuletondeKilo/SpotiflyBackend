from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import RedirectResponse
import common as app_common
from .common import *
from spotipy import SpotifyOAuth, Spotify
from src.app.domain.spotify.models import *
from src.app.infrastructure.external.spotify.schema import *
from fastapi import Depends
from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta
from uuid import uuid4
from .schema import *

login = APIRouter(
    prefix='/v1/login', tags=['login']
)

@login.get("/main")
async def log_in_user():

    auth_manager = SpotifyOAuth(**app_common.SPOTIFY_CONFIG)
    auth_url = auth_manager.get_authorize_url()
    return RedirectResponse(auth_url)

@login.get("/callback")
async def callback(request: Request, db: Session = Depends(get_db)):

    code = request.query_params.get("code")

    auth_manager = SpotifyOAuth(**app_common.SPOTIFY_CONFIG)
    token_info = auth_manager.get_access_token(code)
    sp = Spotify(auth=token_info["access_token"])

    # --- Get user info from Spotify ---
    user_info = sp.current_user()
    user_id = user_info["id"]
    display_name = user_info.get("display_name", "")

    user_data = SpotifyUserSchema(
        id=user_id,
        display_name=display_name
    )

    # --- Insert or fetch SpotifyUser ---
    db_user = db.query(SpotifyUser).filter_by(id=user_id).first()
    if not db_user:
        db_user = SpotifyUser(**vars(user_data))
        db.add(db_user)
        db.commit()
        db.refresh(db_user)

    # --- Create a session ---
    new_session_data = UserSessionSchema(
        session_id=str(uuid4()),  # Generate a new session ID
        user_id=db_user.id,
        created_at=datetime.now(timezone.utc),
        last_active_at=datetime.now(timezone.utc)
    )
    new_session = UserSession(**vars(new_session_data))
    db.add(new_session)
    db.commit()
    db.refresh(new_session)

    # --- Insert associated access token ---
    token_data = AccessTokenSchema(
        session_id=new_session.session_id,
        access_token=token_info["access_token"],
        refresh_token=token_info.get("refresh_token"),
        token_type=token_info.get("token_type", "Bearer"),
        scope=token_info.get("scope"),
        expires_at=datetime.now(timezone.utc) + timedelta(seconds=token_info["expires_in"])
    )
    token = AccessToken(**vars(token_data))
    db.add(token)
    db.commit()

    # Optional: return a success page or session_id
    return AuthCallbackResponseSchema(
        session_id=new_session.session_id,
        user_id=db_user.id,
        display_name=db_user.display_name
    )

@login.delete("/logout/{user_id}")
async def log_off_user(user_id: str, db: Session = Depends(get_db)):
    user = db.query(SpotifyUser).filter(SpotifyUser.id == user_id).first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    # Delete all sessions (and tokens via cascade)
    num_deleted = db.query(UserSession).filter(UserSession.user_id == user_id).delete()
    db.commit()

    return {"message": f"All sessions deleted for user {user_id}.", "sessions_removed": num_deleted}