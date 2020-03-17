from typing import List
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from backend import schemas, crud, config
from backend.utils import get_db, get_current_user, create_access_token
from backend.models import User as DBUser

router = APIRouter()


@router.post("/login", response_model=schemas.Token, tags=["login"])
def login_access_token(
     form_data: schemas.Login,db: Session = Depends(get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not crud.user.is_active(user):
        raise HTTPException(status_code=400, detail="Inactive user")
    access_token_expires = timedelta(minutes=config.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": create_access_token(
            data={"user_id": user.id}, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/user/info", tags=["login"], response_model=schemas.User)
def get_info(current_user: DBUser = Depends(get_current_user)):
    """
    Test access token
    """
    return current_user
