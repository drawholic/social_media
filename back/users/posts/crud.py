from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Posts, PostLikes
from .exceptions import PostDoesNotExist


class PostsCRUD:

    
    def __init__(self, db: AsyncSession) -> None:
        self.db = db


    async def get_post_by_id(self, post_id: int):

        stm = select(Posts).where(Posts.id == post_id)
        res = await self.db.execute(statement=stm)

        return res.scalars().first()

    async def create_post(self, post, user_id:int):

        post = Posts(**post.dict(), user_id=user_id)
        self.db.add(post)
        
        await self.db.commit()


    async def post_detail(self, post_id: int):

        if self.post_exists(post_id=post_id):

            stm = select(Posts).options(selectinload(Posts.comments)).where(Posts.id == post_id)
            res = await self.db.execute(statement=stm)

            return res.scalars().first()


    async def get_posts(self, user_id: int):

        stm = select(Posts).where(Posts.user_id == user_id)
        res = await self.db.execute(stm)

        return res.scalars().all()

    async def post_exists(self, post_id: int):
        post = await self.get_post_by_id(post_id=post_id)

        if post is None:
            raise PostDoesNotExist

        return post


    async def like_a_post(self, post_id: int, user_id: int):

        if await self.post_exists(post_id=post_id):

            post_like = PostLikes(post_id=post_id, user_id=user_id)   

            self.db.add(post_like)
            await self.db.commit()