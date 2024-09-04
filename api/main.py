from fastapi import APIRouter
from .routes import user, auth, post

api_router = APIRouter()

api_router.include_router(auth.router, tags=["auth"])
api_router.include_router(user.router, prefix="/user", tags=["user"])
api_router.include_router(post.router, prefix="/post", tags=["post"])
