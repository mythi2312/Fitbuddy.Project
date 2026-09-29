import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

load_dotenv()

from app.routes import router

BASE_DIR = os.path.dirname(
    os.path.abspath(__file__)
)

app = FastAPI(
    title="FitBuddy - AI Fitness Plan Generator"
)

app.mount(
    "/static",
    StaticFiles(
        directory=os.path.join(
            BASE_DIR,
            "static"
        )
    ),
    name="static"
)

app.include_router(router)
