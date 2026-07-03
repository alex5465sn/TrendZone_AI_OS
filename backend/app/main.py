from fastapi import FastAPI

from backend.app.core.settings import settings
from backend.app.api.system_info import router as system_router
from backend.app.database.base import Base
from backend.app.database.session import engine
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.VERSION,
)
Base.metadata.create_all(bind=engine)

app.include_router(system_router)


@app.get("/")
def home():
    return {
        "status": "online",
        "app": settings.APP_NAME,
        "version": settings.VERSION,
    }