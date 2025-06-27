from fastapi import APIRouter, Body
from schema._input import UserInput
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