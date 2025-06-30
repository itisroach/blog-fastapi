from schema.output import PostOutput
from schema._input import PostInput, PostUpdateInput
from sqlalchemy.ext.asyncio import AsyncSession
from db import UserModel, PostModel
from operations.user import UserOps
from utils.exceptions import NotFoundException, NoAccessToResource
import sqlalchemy as sqa

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



    async def get(self, post_id: int) -> PostOutput:

        query = sqa.select(PostModel).where(PostModel.id == post_id)

        async with self.db as conn:

            result = await conn.scalar(query)

            if result is None:
                raise NotFoundException(PostModel.model_name_for_exceptions)
            
            author = await UserOps(self.db).get_by_username(result.username)

            return PostOutput.show(result, author)
        

    async def get_by_username(self, username: str, page: int) -> list[PostOutput]:

        page_begin = (page * 10) - 10
        
        query = (sqa.select(PostModel)
        .where(sqa.and_(
            PostModel.username == username,
            PostModel.id > page_begin
            )
        )).limit(10)

        results = None

        user = await UserOps(self.db).get_by_username(username)

        async with self.db as conn:

            results = await conn.scalars(query)

            results = results.all()

            if len(results) < 1:
                raise NotFoundException(PostModel.model_name_for_exceptions)


            

        return [PostOutput.show(post, user) for post in results]
    

    async def update(self, updated_data: PostUpdateInput, username: str) -> PostOutput:

        post = await self.get(updated_data.id)
        
        if post.user.username != username:
            raise NoAccessToResource

        dic_fields = {}

        if updated_data.title:
            dic_fields["title"] = updated_data.title

        if updated_data.content:
            dic_fields["content"] = updated_data.content

        query = sqa.update(PostModel).where(PostModel.id == updated_data.id).values(**dic_fields)


        async with self.db as conn:
            await conn.execute(query)
            await conn.commit()

        updated_post = await self.get(updated_data.id)

        return PostOutput.show(updated_post, post.user)
    

    async def delete(self, id: int, username: str):

        post = await self.get(id)

        if post.user.username != username:
            raise NoAccessToResource 


        delete_query = sqa.delete(PostModel).where(PostModel.id == id)

        async with self.db as conn:

            await conn.execute(delete_query)
            await conn.commit()
