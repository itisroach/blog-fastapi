from fastapi.security import OAuth2PasswordBearer
from db.engine import get_db
from utils.jwt import JWTHandler
from typing import Annotated
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends


oauth_scheme = OAuth2PasswordBearer(tokenUrl="token")

async def jwt_required(
    token: str = Depends(oauth_scheme)
):

    decoded_username = await JWTHandler().decode_and_verify_token(token)

    return decoded_username
