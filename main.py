from fastapi import FastAPI
from dotenv import load_dotenv
from src.app.infrastructure.routes.v1.playlist import playlist
from src.app.infrastructure.routes.v1.login import login


# Core Application Instance
app = FastAPI(
    title='SPOTIFLY',
    version='V1.0.0',
)

app.include_router(playlist)
app.include_router(login)
