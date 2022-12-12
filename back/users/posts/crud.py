from sqlalchemy import select, and_, func
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import Posts, PostLikes

from .exceptions import PostDoesNotExist, PostAlreadyLiked, PostNotLiked
from typing import List, Union


class PostsCRUD:

    
    def __init__(self, db: AsyncSession) -> None:
        self.db = db


    async def get_post_by_id(self, post_id: int) -> Posts:

        stm = select(Posts).where(Posts.id == post_id)
        res = await self.db.execute(statement=stm)

        return res.scalars().first()


    async def create_post(self, post, user_id:int) -> None:

        post = Posts(**post.dict(), user_id=user_id)
        self.db.add(post)
        
        await self.db.commit()


    async def post_detail(self, post_id: int) -> Union[Posts, None]:

        if self.post_exists(post_id=post_id):

            stm = select(Posts).options(selectinload(Posts.comments)).where(Posts.id == post_id)
            res = await self.db.execute(statement=stm)

            return res.scalars().first()


    async def get_posts(self, user_id: int) -> List[Posts]:

        stm = select(Posts).where(Posts.user_id == user_id)
        res = await self.db.execute(stm)

        return res.scalars().all()


    async def post_exists(self, post_id: int) -> Posts:
        post = await self.get_post_by_id(post_id=post_id)

        if post is None:
            raise PostDoesNotExist

        return post

    async def _get_post_likes(self, post_id: int):
        count = select([func.count()]).select_from(PostLikes).where(PostLikes.post_id == post_id).scalar()
        # res = await self.db.execute(stm)
        # count = res.scalar()
        return count 
        

    async def _get_post_like(self, post_id: int, user_id: int) -> PostLikes:
        stm = select(PostLikes).where(and_(PostLikes.post_id == post_id, PostLikes.user_id == user_id))
        res = await self.db.execute(stm)
        post_like = res.scalars().first()
        return post_like        


    async def like_a_post(self, post_id: int, user_id: int) -> None:

        await self.post_exists(post_id=post_id)
        if await self._get_post_like(post_id=post_id, user_id=user_id):
            raise PostAlreadyLiked   

        post_like = PostLikes(post_id=post_id, user_id=user_id)   

        self.db.add(post_like)
        await self.db.commit()
    
    async def unlike_a_post(self, post_id: int, user_id: int):
        await self.post_exists(post_id=post_id)
        if not (await self._get_post_like(post_id=post_id, user_id=user_id)):
            raise PostNotLiked


        post = await self._get_post_like(user_id=user_id, post_id=post_id)
        await self.db.delete(post)
        await self.db.commit()