from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .api_endpoints import auth, like, piece, user
from .core import database
from .core.database import engine


database.Base.metadata.create_all(bind=engine) # We don't need that if we use Alembic

app = FastAPI()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],
#     allow_credentials=True,
#     allow_methods=["*"],
#     allow_headers=["*"],
# )

app.include_router(auth.router)
app.include_router(like.router)
app.include_router(piece.router)
app.include_router(user.router)

@app.get("/", tags=["Root"])
def read_root():
    """Welcome endpoint for the NovelNest API."""
    return {
        "message": "Welcome to NovelNest API",
        "version": "1.0.0",
        "docs": "/docs"
    }

