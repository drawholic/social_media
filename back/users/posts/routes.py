from fastapi import APIRouter, Depends
from db.db import get_db
from .crud import PostsCRUD
from .pd import PostCreate, Post


posts = APIRouter(prefix="/posts", tags=['Posts'])


@posts.get("/{user_id}")
async def get_posts(user_id: int, db = Depends(get_db)):
    return await PostsCRUD(db).get_posts(user_id=user_id)


@posts.get("/detail/{post_id}")
async def post_detail(post_id: int, db = Depends(get_db)):
    return await PostsCRUD(db).post_detail(post_id=post_id)


@posts.post("", status_code=201)
async def create_post(post: PostCreate, db = Depends(get_db)):
    await PostsCRUD(db).create_post(post=post)


@posts.post("/{post_id}/")
async def like_a_post(post_id: int, db = Depends(get_db)):
    await PostsCRUD(db).like_a_post(post_id=post_id)


# @posts.delete("/{post_id}/")