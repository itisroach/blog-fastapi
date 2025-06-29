from fastapi import APIRouter, Depends, Body, Response, status
from operations.user import UserOps
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import get_db
from utils.dependency import jwt_required
from schema._input import UpdateUserInput

router = APIRouter()



@router.get("/get/{username}/")
async def get_user(
    username: str,
    depends_tuple: tuple = Depends(jwt_required),
):

    db_session, _ = depends_tuple

    user = await UserOps(db_session).get_by_username(username)

    return user


@router.put("/update")
async def update_user(
    depends_tuple: tuple = Depends(jwt_required),
    body: UpdateUserInput = Body(),
):
    
    db_session, username = depends_tuple

    user = await UserOps(db_session).update(username, body)

    return user


@router.delete("/delete")
async def delete_user(
    response: Response,
    depends_tuple: tuple = Depends(jwt_required),
):

    db_session, username = depends_tuple

    await UserOps(db_session).delete(username)

    response.status_code = status.HTTP_204_NO_CONTENT