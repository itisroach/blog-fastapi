from schema.output import PostOutput
from schema._input import PostInput
from sqlalchemy.ext.asyncio import AsyncSession
from db import UserModel, PostModel
from operations.user import UserOps

class PostOps:

    def __init__(self, db_session: AsyncSession):
        self.db = db_session

    
    async def create(self, post_data: PostInput, username: str) -> PostOutput:

        post_instance = PostModel(
            username=username,
            title=post_data.title,
            content=post_data.content,
        )

        user = await UserOps(self.db).get_by_username(username)

        async with self.db as conn:
            conn.add(post_instance)
            await conn.commit()


        return PostOutput.show(post_instance, user)
