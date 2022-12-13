from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer 


auth = APIRouter(prefix='/auth', tags=["Auth"])

scheme = OAuth2PasswordBearer(tokenUrl="/auth/get_token")


@auth.post("/get_token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(),
                    db = Depends(get_db)
):
    email = form_data.username
    password = form_data.password
    user = await UserCRUD(db).get_user_for_auth(email=email, password=password)
    if user is None:
        raise AuthException
    token = generate_token(payload=email)
    return {"token": token} 

