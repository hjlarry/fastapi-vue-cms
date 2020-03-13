from fastapi import APIRouter

from . import article
from . import user

api_router = APIRouter()
api_router.include_router(article.router, prefix="/articles", tags=["articles"])
api_router.include_router(user.router, prefix="/users", tags=["users"])