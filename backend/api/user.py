from typing import List, Any


from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import schemas, crud
from backend.utils import get_db, MyResponse

router = APIRouter()


@router.post("/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.user.get_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return crud.user.create(db, obj_in=user)


@router.get("/", response_model=List[schemas.User], response_class=MyResponse)
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


@router.get("/{user_id}", response_model=schemas.User)
def read_user(user_id: int, db: Session = Depends(get_db)):
    db_user = crud.user.get(db, user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user
