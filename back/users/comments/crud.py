from sqlalchemy.ext.asyncio import AsyncSession
from .pd import CommentCreate
from db.models import Comments, CommentLikes
from sqlalchemy import select, exists


class CommentCRUD:

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def list(self, post_id: int):
        stm = select(Comments).where(Comments.post_id == post_id)
        res = await self.db.execute(stm)
        return res.scalars().all()

    async def create_comment(self, comment: CommentCreate):
        stm = Comments(**comment.dict())
        self.db.add(stm)
        await self.db.commit()
    
    async def comment_exists(self, comment_id: int):
        stm = exists(Comments).where(Comments.id == comment_id)
        res = await self.db.execute(statement=stm)
        comment_exists = res.scalars().first()
        print("COMMENT EXISTS: ", comment_exists)
    
    async def like_comment(self, comment_id: int):
        stm = select(Comments).where(Comments.id == comment_id)
        res = await self.db.execute(stm)
        comment = res.scalars().first()
        
