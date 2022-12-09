from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from db.models import Users
from .pd import UserCreate
from .exceptions import UserAlreadyExists
from typing import List, Union


class UserCRUD:


    def __init__(self, db: AsyncSession) -> None:
        self.db = db


    def _user_by_id_query(self, id: int):
        stm = select(Users).where(Users.id == id)
        return stm


    def _user_by_email_query(self, email: str):
        stm = select(Users).where(Users.email == email)
        return stm

    def _user_detail_by_id_query(self, user_id: int):
        stm = select(Users).options(selectinload(Users.posts)).where(Users.id == user_id)
        return stm


    async def get_user_by_email(self, email: str) -> Users:
        stm = self._user_by_email_query(email=email)

        res = await self.db.execute(statement=stm)
        return res.scalars().first()


    async def get_user_by_id(self, id: int) -> Users:
        stm = self._user_by_id_query(id=id)

        res = await self.db.execute(statement=stm)
        return res.scalars().first()

    

    async def user_detail(self, user_id: int):
        stm = self._user_detail_by_id_query(user_id=user_id)
        res = await self.db.execute(stm)
        return res.scalars().first()


    async def create(self, user_data: UserCreate) -> None:
        if await self.get_user_by_email(email=user_data.email) is not None:
            raise UserAlreadyExists

        stm = Users(email=user_data.email, password=user_data.password1)
        self.db.add(stm)
        await self.db.commit()


    async def list_users(self) -> Union[List[Users], None]:
        stm = select(Users).where(Users.is_active == True)
        res = await self.db.execute(stm)
        users = res.scalars().all()
        return  users