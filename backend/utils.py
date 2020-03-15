import json
from datetime import datetime, timedelta
from typing import Any

import jwt
from starlette.requests import Request
from starlette.responses import JSONResponse
from starlette.status import HTTP_403_FORBIDDEN
from passlib.context import CryptContext
from fastapi import Depends, Security, HTTPException
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from backend import crud, config
from backend.schemas import TokenPayload

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
reusable_oauth2 = OAuth2PasswordBearer(tokenUrl="/api/v1/login/access-token")


def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str):
    return pwd_context.hash(password)


def get_db(request: Request):
    return request.state.db


def get_current_user(
    db: Session = Depends(get_db), token: str = Security(reusable_oauth2)
):
    try:
        payload = jwt.decode(token, config.SECRET_KEY, algorithms=[ALGORITHM])
        token_data = TokenPayload(**payload)
    except jwt.PyJWTError:
        raise HTTPException(
            status_code=HTTP_403_FORBIDDEN, detail="Could not validate credentials"
        )
    user = crud.user.get(db, id=token_data.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user


ALGORITHM = "HS256"
access_token_jwt_subject = "access"


def create_access_token(*, data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire, "sub": access_token_jwt_subject})
    encoded_jwt = jwt.encode(to_encode, config.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


class MyResponse(JSONResponse):
    def render(self, content: Any) -> bytes:
        my_content = {
            "code": 0,
            "data": content,
        }
        return json.dumps(
            my_content,
            ensure_ascii=False,
            allow_nan=False,
            indent=None,
            separators=(",", ":"),
        ).encode("utf-8")
