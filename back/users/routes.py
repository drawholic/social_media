from typing import List

from fastapi import APIRouter, Depends

from db.db import get_db
from .crud import UserCRUD  
from .pd import User, UserCreate, UserDetail
from .exceptions import UserDoesNotExist


users = APIRouter(prefix="/users", tags=["Users"])


@users.get("/{user_id}", response_model=User)
async def retrieve_id(user_id: int, db = Depends(get_db)):

    user = await UserCRUD(db).get_user_by_id(id=user_id)

    if user is None:
        raise UserDoesNotExist
    
    return user


@users.get('/{user_id}/detail', response_model=UserDetail)
async def detail(user_id: int, db = Depends(get_db)):
    user = await UserCRUD(db).user_detail(user_id=user_id)

    if user is None:
        raise UserDoesNotExist

    return user


@users.get("/", response_model=List[User])
async def list_users(db = Depends(get_db)):

    return await UserCRUD(db).list_users()


@users.post("/create" ,status_code=201)
async def create(user_data: UserCreate, db = Depends(get_db)):

    await UserCRUD(db).create(user_data=user_data)