from fastapi import FastAPI

import setup
from api import user

setup.setup_env()

app = FastAPI(title="AI Nerd Podcast")

app.include_router(user.router, prefix="/user", tags=["User"])
