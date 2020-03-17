from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from backend import schemas, crud
from backend.utils import get_db

router = APIRouter()


@router.post("/users/{user_id}/articles/", response_model=schemas.Article)
def create(user_id: int, article: schemas.ArticleCreate, db: Session = Depends(get_db)):
    return crud.article.create_with_owner(db, obj_in=article, owner_id=user_id)


@router.get("", response_model=List[schemas.Article])
def read_articles(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    items = crud.article.get_multi(db, skip=skip, limit=limit)
    return items
