from fastapi import APIRouter
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer


auth = APIRouter(prefix='/auth', tags=["Auth"])

scheme = OAuth2PasswordBearer(tokenUrl="/get_token")


@auth.post("/get_token")
async def get_token(form_data: OAuth2PasswordRequestForm())