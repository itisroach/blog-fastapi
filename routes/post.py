from fastapi import APIRouter, Response, Depends, status, Body
from utils.dependency import jwt_required
from operations.post import PostOps
from schema._input import PostInput


router = APIRouter()


@router.post("/write")
async def create_new_post(
    response: Response,
    depends_tuple: tuple = Depends(jwt_required),
    body: PostInput = Body()
):
    
    db_session, username = depends_tuple


    result = await PostOps(db_session).create(body, username)

    response.status_code = status.HTTP_201_CREATED

    return result