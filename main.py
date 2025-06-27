from fastapi import FastAPI
from routes import user
from contextlib import asynccontextmanager
from typing import AsyncGenerator
from db.engine import engine, Base

@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

    yield


app = FastAPI(lifespan=lifespan)


app.include_router(
    router=user.router,
    prefix="/auth"
)


@app.get("/")
async def hello():
    return {"message": "hello world"} 