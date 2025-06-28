from fastapi import APIRouter, Body
from schema._input import UserInput, UserLoginInput, UserRefreshTokenInput
from operations.user import UserOps
from sqlalchemy.ext.asyncio import AsyncSession
from typing import Annotated
from db.engine import get_db
from fastapi import Depends



router = APIRouter()

@router.post("/register")
async def register(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    body: UserInput = Body(),
):

    user = await UserOps(db_session).create(body)

    return user


@router.post("/login")
async def login(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    body: UserLoginInput = Body(),
):
    
    result = await UserOps(db_session).login(body)

    return result



@router.post("/refresh-token")
async def refresh_token(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    body: UserRefreshTokenInput = Body(),
):
    jwt_tokens = await UserOps(db_session).refresh_token(body.token)

    return jwt_tokens