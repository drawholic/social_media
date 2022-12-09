from sqlalchemy import select
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Posts


class PostsCRUD:

    
    def __init__(self, db: AsyncSession) -> None:
        self.db = db


    async def create_post(self, post):
        post = Posts(**post.dict())
        self.db.add(post)
        await self.db.commit()


    async def post_detail(self, post_id: int):
        stm = select(Posts).options(selectinload(Posts.comments)).where(Posts.id == post_id)
        res = await self.db.execute(statement=stm)
        return res.scalars().first()


    async def get_posts(self, user_id: int):
        stm = select(Posts).where(Posts.user_id == user_id)
        res = await self.db.execute(stm)
        return res.scalars().all()


    async def like_a_post(self, post_id: int):
        stm = select(Posts).where(Posts.id == post_id)
        res = await self.db.execute(stm)
        post = res.scalars().first()
        post.likes = post.likes + 1
        await self.db.commit()
        