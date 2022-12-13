from fastapi import FastAPI, Depends
from fastapi.security import OAuth2PasswordRequestForm
from db.db import engine, get_db
from db.models import Base
from users.crud import UserCRUD
from users.auth.exceptions import AuthException
from users.auth.utils import generate_token
from users.routes import users
from users.posts.routes import posts
from users.comments.routes import comments 

app = FastAPI()

app.include_router(users)
app.include_router(posts)
app.include_router(comments) 


async def init_models():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


@app.on_event("startup")
async def startup():
    await init_models()

@app.get("/")
async def index():
    return {"Status": "Working"}



@app.post("/token")
async def get_token(form_data: OAuth2PasswordRequestForm = Depends(),
                    db = Depends(get_db)
):
    email = form_data.username
    password = form_data.password  
    user = await UserCRUD(db).get_user_for_auth(email=email, password=password)
    if user is None:
        raise AuthException
    token = generate_token(payload=email) 
    return {"access_token": token, "token_type": "bearer"}