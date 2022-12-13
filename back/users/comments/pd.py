from pydantic import BaseModel


class CommentBase(BaseModel):
    text: str


class CommentCreate(CommentBase):
    post_id: int 


class Comment(CommentCreate):
    id: int

    class Config:
        orm_mode = True
