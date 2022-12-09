from pydantic import BaseModel, EmailStr, validator
from datetime import datetime
from typing import List, Union
from .exceptions import PasswordsDoNotMatch 
from .posts.pd import Post


class UserBase(BaseModel):
    email: EmailStr


class UserCreate(UserBase):
    password1: str
    password2: str

    @validator("password2", allow_reuse=True)
    def passwords_match(cls, v, values):
        if "password1" not in values and v != values['password1']:
            raise PasswordsDoNotMatch
        return v


class User(UserBase):
    id: int
    created_at: datetime
    updated_at: Union[datetime, None] 

    class Config:
        orm_mode = True


class UserDetail(User):
    posts: List[Post] = []


class UserList(BaseModel):
    users: List[User] = []

    class Config:
        orm_mode = True