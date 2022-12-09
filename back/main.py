from fastapi import FastAPI 
from db.db import engine
from db.models import Base
from users.routes import users
from users.posts.routes import posts
from users.comments.routes import comments
from users.auth.routes import auth

app = FastAPI()

app.include_router(users)
app.include_router(posts)
app.include_router(comments)
app.include_router(auth)


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



