from schema._input import (
    UserInput, 
    UserLoginInput, 
    UpdateUserInput
)
from schema.output import (
    UserOutput, 
    JWTOutput, 
    UserUpdateOutput
)
from sqlalchemy.ext.asyncio import AsyncSession
from db import UserModel
import sqlalchemy as sqa
from utils.jwt import JWTHandler
from sqlalchemy.exc import IntegrityError
from utils.crypt import hash_password, compare_password
from utils.exceptions import (
    NotFoundException, 
    DuplicateException,
    UsernameOrPasswordException,
    NoFieldWerePassed
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

    async def get_by_username(self, username: str) -> UserOutput:

        select_query = sqa.select(UserModel).where(UserModel.username == username)

        async with self.db as conn:

            user = await conn.scalar(select_query)

            if user is None:
                raise NotFoundException(UserModel.model_name_for_exceptions)
            
            return UserOutput.show(user)
        

    async def refresh_token(self, token: str) -> JWTOutput:

        username = await JWTHandler(self.db).decode_and_verify_token(token, True)

        result = await JWTHandler(self.db).generate(username)

        return result
    

    async def update(self, old_username: str , updated_data: UpdateUserInput) -> UserOutput | UserUpdateOutput:

        update_fields = {}

        if updated_data.username is not None:
            update_fields["username"] = updated_data.username

        if updated_data.name is not None:
            update_fields["name"] = updated_data.name
        

        if not update_fields:
            raise NoFieldWerePassed

        update_query = sqa.update(UserModel).where(UserModel.username == old_username).values(**update_fields)


        async with self.db as conn:
            
            result = await conn.execute(update_query)
            await conn.commit()
            

            if result.rowcount == 0:
                raise NotFoundException(UserModel.model_name_for_exceptions)

        username_to_fetch = updated_data.username if updated_data.username else old_username

        updated_user = await self.get_by_username(username_to_fetch)

        if updated_data.username:
    
            jwt = await JWTHandler(self.db).generate(username_to_fetch)

            return UserUpdateOutput(user=updated_user, token=jwt)
        

        return updated_user
    
    async def delete(self, username: str):
        print(username)
        delete_query = sqa.delete(UserModel).where(UserModel.username == username)

        async with self.db as conn:

            result = await conn.execute(delete_query)
            await conn.commit()

            if result.rowcount == 0:
                
                raise NotFoundException(UserModel.model_name_for_exceptions)
            



            