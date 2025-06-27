from schema._input import UserInput 
from sqlalchemy.ext.asyncio import AsyncSession
from db import UserModel
from sqlalchemy.exc import IntegrityError
from utils.crypt import hash_password
from utils.exceptions import NotFoundException, DuplicateException



class UserOps:

    def __init__(self, db_connection: AsyncSession) -> None:
        self.db = db_connection        


    async def create(self, user_data: UserInput) -> UserModel:
        
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

        return user