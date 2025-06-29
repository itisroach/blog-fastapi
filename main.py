from fastapi import FastAPI
from routes import auth, user, post
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from db.engine import engine, Base


# initilizing database on start app in Fast API's life span
@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)

# including routes with prefix from other files 
app.include_router(
    router=auth.router,
    prefix="/auth"
)

app.include_router(
    router=user.router,
    prefix="/users"
)
app.include_router(
    router=post.router,
    prefix="/posts"
)

@app.get("/")
async def hello():
    return {"message": "hello world"} 