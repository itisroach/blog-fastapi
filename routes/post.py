from fastapi import APIRouter, Response, Depends, status, Body
from utils.dependency import jwt_required
from db.engine import get_db
from sqlalchemy.ext.asyncio import AsyncSession
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


@router.get("/get/{post_id}")
async def get_post(
    post_id: int,
    db_session: AsyncSession = Depends(get_db),
):

    post = await PostOps(db_session).get(post_id)

    return post


@router.get("/{username}/get")
async def get_post_by_username(
    username: str,
    page: int = 1,
    db_session: AsyncSession = Depends(get_db)
):
    
    result = await PostOps(db_session).get_by_username(username, page)

    return result