from fastapi.security import OAuth2PasswordBearer
from db.engine import get_db
from utils.jwt import JWTHandler
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def jwt_required(
    db_session: Annotated[AsyncSession, Depends(get_db)],
    token: str = Depends(oauth_scheme)
):

    decoded_username = await JWTHandler(db_session).decode_and_verify_token(token)

    return (db_session, decoded_username)
