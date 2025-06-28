from fastapi import APIRouter, Depends
from operations.user import UserOps
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from db.engine import get_db


router = APIRouter()



@router.get("/{username}/")
async def get_user(
    username: str,
    db_session: Annotated[AsyncSession, Depends(get_db)] 
):
    
    user = await UserOps(db_session).get_by_username(username)

    return user