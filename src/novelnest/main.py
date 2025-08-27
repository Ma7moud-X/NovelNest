from fastapi import FastAPI

from .routers import piece
from . import db_models
from .database import engine


db_models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.include_router(piece.router)


@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint for the NovelNest API."""
    return {
        "message": "Welcome to NovelNest API",
        "version": "1.0.0",
        "docs": "/docs"
    }

