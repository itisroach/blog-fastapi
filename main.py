from fastapi import FastAPI
from routes import user


app = FastAPI()


app.include_router(
    router=user.router,
    prefix="/auth"
)


@app.get("/")
async def hello():
    return {"message": "hello world"} 