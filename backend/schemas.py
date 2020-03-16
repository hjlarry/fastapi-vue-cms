from typing import List, Optional

from pydantic import BaseModel


class ArticleBase(BaseModel):
    title: str
    content: str = None


class ArticleCreate(ArticleBase):
    title: str


class ArticleUpdate(ArticleBase):
    pass


class ArticleInDBBase(ArticleBase):
    id: int
    title: str
    owner_id: int

    class Config:
        orm_mode = True


class Article(ArticleInDBBase):
    pass


class ArticleInDB(ArticleInDBBase):
    pass


class UserBase(BaseModel):
    email: Optional[str] = None
    is_active: Optional[bool] = True
    is_superuser: Optional[bool] = False


class UserBaseInDB(UserBase):
    id: int = None

    class Config:
        orm_mode = True


# Properties to receive via API on creation
class UserCreate(UserBaseInDB):
    email: str
    password: str


# Properties to receive via API on update
class UserUpdate(UserBaseInDB):
    password: Optional[str] = None


# Additional properties to return via API
class User(UserBaseInDB):
    pass


# Additional properties stored in DB
class UserInDB(UserBaseInDB):
    hashed_password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    user_id: int = None

class Login(BaseModel):
    username: str
    password: str