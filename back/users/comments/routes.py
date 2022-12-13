from fastapi import APIRouter, Depends
from db.db import get_db
from .crud import CommentCRUD
from .pd import CommentCreate, Comment
from typing import List
from users.auth.routes import scheme
from users.auth.utils import is_auth

comments = APIRouter(prefix="/comments", tags=["Comments"])


@comments.post("/", status_code=201)
async def create_comment(
    comment: CommentCreate,
     db = Depends(get_db),
     token = Depends(scheme)
     ):
     
    user = await is_auth(token=token, db=db)
    await CommentCRUD(db).create_comment(comment=comment, user_id= user.id)


@comments.get("/{post_id}", response_model=List[Comment])
async def list_comments(post_id: int, db = Depends(get_db)):
    return await CommentCRUD(db).list(post_id=post_id)
    