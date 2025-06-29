import jwt
from datetime import datetime, timedelta
from settings import ALGORITHM, SECRET
from schema.output import JWTOutput
from utils.exceptions import InvalideTokenException
from sqlalchemy.ext.asyncio import AsyncSession
from db.models import TokenModel
import sqlalchemy as sqa


# a class for handling functionalities of jwt tokens
class JWTHandler:

    def __init__(self, db_session: AsyncSession):
        self.db_session = db_session


    # generating a JWT token based on username
    async def generate(self, username: str, exp_time: datetime = None) -> JWTOutput:

        """
            generating an access and a refresh token for given credentials
        """


        # checking if user got any token recorded on database and if they do it will be deleted
        token_exists = await self.check_token_existance(username)
        
        if token_exists:
            await self.delete_from_db(username)



        # if expire time set it will be also set on jwt token and if not it will be set from on day from now by default
        exp_time = exp_time if exp_time else datetime.now() + timedelta(days=1)

        exp_time = int(exp_time.timestamp()) # turning the time to whole seconds

        payload = {
            "exp": exp_time,
            "username": username,
            "token_type": "access"
        }

        access_token = jwt.encode(payload, key=SECRET, algorithm=ALGORITHM) # creating access token

    
        refresh_token, payload = self.generate_referesh_token(username) # generating refresh token
        
        await self.add_token_to_db(refresh_token, payload["exp"], payload["username"]) # adding refresh token to database

        return JWTOutput(access=access_token, refresh=refresh_token)


    def generate_referesh_token(self, username: str):
        # setting expiration time to two days from now by default
        exp_time = datetime.now() + timedelta(days=2)
        
        payload = {
            "exp": int(exp_time.timestamp()),
            "username": username,
            "token_type": "refresh"
        }

        refresh_token = jwt.encode(payload, key=SECRET, algorithm=ALGORITHM)

        return (refresh_token, payload)
    

    async def decode_and_verify_token(self, token: str, is_refresh_token: bool = False) -> str:

        """
            getting username by decoding jwt token and verifying if the token is valid or not
        """


        # decoding the jwt payload and raising any error related to jwt token itself
        try:
            value = jwt.decode(token, key=SECRET, algorithms=[ALGORITHM])

        except jwt.exceptions.InvalidTokenError as e:
            
            raise InvalideTokenException(str(e))
        
        # checking if the token which is being decoded is a refresh token or an access token
        if is_refresh_token:
            # it access token passed it will raise an error 
            if value["token_type"] == "access": 
                raise InvalideTokenException("the give token is access token, you should pass refresh token")

            # checking if refresh token exists into database records
            token_exists = await self.check_token_existance(token=token)

            # if refresh token does not exist so it's an invalid token or used once before
            if not token_exists:
                raise InvalideTokenException("refresh token should be used once, use fresh refresh token instead")


        # using user operations to check if user in decoded access token is an existed user or not (import is here due to circular import)
        from operations.user import UserOps

        await UserOps(self.db_session).get_by_username(value["username"])


        return value["username"]
    

    async def delete_from_db(self, username: str):

        """
            deleting refresh token from database or in other way making it invalid
        """

        delete_query = sqa.delete(TokenModel).where(TokenModel.username == username)

        async with self.db_session as conn:
            await conn.execute(delete_query)
            await conn.commit()


    async def add_token_to_db(self, token: str, exp: int, username: str):

        """
            add a fresh refresh token to database
        """

        token_instance = TokenModel(username=username, expiration=exp, refresh_token=token)

        async with self.db_session as conn:
            conn.add(token_instance)
            await conn.commit()


    async def check_token_existance(self, username: str = None, token: str = None) -> bool:

        """
            check if token exists returns True if token exists and if not False
        """

        query = sqa.select(TokenModel).where(sqa.or_(
            TokenModel.username == username, 
            TokenModel.refresh_token == token,
        ))

        async with self.db_session as conn:

            result = await conn.scalar(query)

            if result is None:
                return False

        return True