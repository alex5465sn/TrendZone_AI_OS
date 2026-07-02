from fastapi import FastAPI

from backend.app.core.settings import settings
from backend.app.database.init_db import init_database

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)

init_database()


@app.get("/")
def home():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
    }