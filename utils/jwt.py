import jwt
from datetime import datetime, timedelta
from settings import ALGORITHM, SECRET
from schema.output import JWTOutput
from utils.exceptions import InvalideTokenException
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import TokenModel
import sqlalchemy as sqa


class JWTHandler:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session

    async def generate(self, username: str, exp_time: datetime = None) -> JWTOutput:

        token_exists = await self.check_token_existance(username)
        
        if token_exists:
            await self.delete_from_db(username)


        exp_time = exp_time if exp_time else datetime.now() + timedelta(days=1)

        exp_time = int(exp_time.timestamp())

        payload = {
            "exp": exp_time,
            "username": username,
            "token_type": "access"
        }

        access_token = jwt.encode(payload, key=SECRET, algorithm=ALGORITHM)

    
        refresh_token, payload = self.generate_referesh_token(username)
        
        await self.add_token_to_db(refresh_token, payload["exp"], payload["username"])

        return JWTOutput(access=access_token, refresh=refresh_token)


    def generate_referesh_token(self, username: str):
        exp_time = datetime.now() + timedelta(minutes=1)
        
        payload = {
            "exp": int(exp_time.timestamp()),
            "username": username,
            "token_type": "refresh"
        }

        refresh_token = jwt.encode(payload, key=SECRET, algorithm=ALGORITHM)

        return (refresh_token, payload)
    

    async def decode_and_verify_token(self, token: str, is_refresh_token: bool = False) -> str:

        try:
            value = jwt.decode(token, key=SECRET, algorithms=[ALGORITHM])

        except jwt.exceptions.InvalidTokenError as e:
            
            raise InvalideTokenException(str(e))
        
    
        if is_refresh_token:
            if value["token_type"] == "access": 
                raise InvalideTokenException("the give token is access token, you should pass refresh token")
        
            token_exists = await self.check_token_existance(token=token)


            if not token_exists:
                raise InvalideTokenException("refresh token should be used once, use fresh refresh token instead")


        return value["username"]
    

    async def delete_from_db(self, username: str):

        delete_query = sqa.delete(TokenModel).where(TokenModel.username == username)

        async with self.db_session as conn:
            await conn.execute(delete_query)
            await conn.commit()


    async def add_token_to_db(self, token: str, exp: int, username: str):

        token_instance = TokenModel(username=username, expiration=exp, refresh_token=token)

        async with self.db_session as conn:
            conn.add(token_instance)
            await conn.commit()


    async def check_token_existance(self, username: str = None, token: str = None) -> bool:

        query = sqa.select(TokenModel).where(sqa.or_(
            TokenModel.username == username, 
            TokenModel.refresh_token == token,
        ))

        async with self.db_session as conn:

            result = await conn.scalar(query)

            if result is None:
                return False

        return True