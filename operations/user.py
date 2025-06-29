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
        
        """
            create and saves an user instance to database
        """

        # hashing user password before saving to database
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

            # if username is duplicated
            except IntegrityError:
                raise DuplicateException(user.model_name_for_exceptions)

        return UserOutput.show(user)
    

    async def login(self, user_data: UserLoginInput) -> JWTOutput:
        

        """
            checks for user existance and if they exist it will compare hashed password and grant access by returning jwt tokens
        """

        # making query for database
        select_query = sqa.select(UserModel).where(UserModel.username == user_data.username)

        async with self.db as conn:
            # running query on database
            user = await conn.scalar(select_query)

            # if username not exists
            if user is None:
                raise UsernameOrPasswordException
            # if password is wrong
            if not compare_password(user_data.password, user.password):
                raise UsernameOrPasswordException

        # if login was successful generates jwt tokens
        result = await JWTHandler(self.db).generate(username=user_data.username)
    
        return result

    async def get_by_username(self, username: str) -> UserOutput:


        """
            querying user by their username
        """


        select_query = sqa.select(UserModel).where(UserModel.username == username)

        async with self.db as conn:

            user = await conn.scalar(select_query)

            if user is None:
                raise NotFoundException(UserModel.model_name_for_exceptions)
            
            return UserOutput.show(user)
        

    async def refresh_token(self, token: str) -> JWTOutput:

        """
            refreshing user's tokens
        """

        username = await JWTHandler(self.db).decode_and_verify_token(token, True)

        result = await JWTHandler(self.db).generate(username)

        return result
    

    async def update(self, old_username: str , updated_data: UpdateUserInput) -> UserOutput | UserUpdateOutput:


        """
            update user informations, if username were updated it will generate new jwt tokens and if not it will only return user updated information
        """


        update_fields = {}

        # fields are optional and we will check which fields are used for update request
        if updated_data.username is not None:
            update_fields["username"] = updated_data.username

        if updated_data.name is not None:
            update_fields["name"] = updated_data.name
        
        # if all fields are empty
        if not update_fields:
            raise NoFieldWerePassed

        # making update query
        update_query = sqa.update(UserModel).where(UserModel.username == old_username).values(**update_fields)


        async with self.db as conn:
            
            result = await conn.execute(update_query)
            await conn.commit()
            
            # checking if any row were affected
            if result.rowcount == 0:
                raise NotFoundException(UserModel.model_name_for_exceptions)

        # getting username of user who were requested update
        username_to_fetch = updated_data.username if updated_data.username else old_username

        # get user updated user for diplaying to user
        updated_user = await self.get_by_username(username_to_fetch)

        # if username was updated it will generate new refresh token
        if updated_data.username:
    
            jwt = await JWTHandler(self.db).generate(username_to_fetch)

            return UserUpdateOutput(user=updated_user, token=jwt)
        

        return updated_user
    
    async def delete(self, username: str):
        

        """
            deleting user from database by their username
        """


        delete_query = sqa.delete(UserModel).where(UserModel.username == username)

        async with self.db as conn:

            result = await conn.execute(delete_query)
            await conn.commit()

            if result.rowcount == 0:
                
                raise NotFoundException(UserModel.model_name_for_exceptions)
            



            