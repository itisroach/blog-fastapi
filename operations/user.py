from schema._input import UserInput, UserLoginInput
from schema.output import UserOutput, JWTOutput
from sqlalchemy.ext.asyncio import AsyncSession
from db import UserModel
import sqlalchemy as sqa
from utils.jwt import JWTHandler
from sqlalchemy.exc import IntegrityError
from utils.crypt import hash_password, compare_password
from utils.exceptions import (
    NotFoundException, 
    DuplicateException,
    UsernameOrPasswordException
)



class UserOps:

    def __init__(self, db_connection: AsyncSession) -> None:
        self.db = db_connection        


    async def create(self, user_data: UserInput) -> UserOutput:
        
        hashed_password = hash_password(user_data.password)


        user = UserModel(
            username=user_data.username, 
            name=user_data.name,
            password=hashed_password,
        )

        async with self.db as conn:
            
            try:
                conn.add(user)
                await conn.commit()

            except IntegrityError:
                raise DuplicateException(user.model_name_for_exceptions)

        return UserOutput.show(user)
    

    async def login(self, user_data: UserLoginInput) -> JWTOutput:
        
        select_query = sqa.select(UserModel).where(UserModel.username == user_data.username)

        async with self.db as conn:

            user = await conn.scalar(select_query)

            if user is None:
                raise UsernameOrPasswordException
            
            if not compare_password(user_data.password, user.password):
                raise UsernameOrPasswordException


        result = await JWTHandler(self.db).generate(username=user_data.username)
    
        return result

    async def get_by_username(self, username: str) -> UserModel:

        select_query = sqa.select(UserModel).where(UserModel.username == username)

        async with self.db as conn:

            user = await conn.scalar(select_query)

            if user is None:
                raise NotFoundException(UserModel.model_name_for_exceptions)
            
            return UserOutput.show(user)
        

    async def refresh_token(self, token: str) -> JWTOutput:

        username = await JWTHandler(self.db).decode_and_verify_token(token)

        result = await JWTHandler(self.db).generate(username)

        return result
