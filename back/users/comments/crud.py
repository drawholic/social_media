from sqlalchemy.ext.asyncio import AsyncSession
from .pd import CommentCreate
from db.models import Comments
from sqlalchemy import select


class CommentCRUD:

    def __init__(self, db: AsyncSession):
        self.db = db
    
    async def list(self, post_id: int):
        stm = select(Comments).where(Comments.post_id == post_id)
        res = await self.db.execute(stm)
        return res.scalars().all()

    async def create_comment(self, comment: CommentCreate, user_id: int):
        stm = Comments(**comment.dict(), user_id=user_id)
        self.db.add(stm)
        await self.db.commit()
    
    async def like_comment(self, comment_id: int):
        stm = select(Comments).where(Comments.id == comment_id)
        res = await self.db.execute(stm)
        comment = res.scalars().first()
        comment.likes = comment.likes + 1
        await self.db.commit()

