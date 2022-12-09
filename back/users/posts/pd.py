from pydantic import BaseModel
from ..comments.pd import Comment
from typing import List

class PostBase(BaseModel):
    text: str

class PostCreate(PostBase):
    pass

class Post(PostCreate):
    likes: int
    id: int
    comments: List[Comment] = []

    class Config:
        orm_mode = True