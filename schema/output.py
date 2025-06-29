from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from db import UserModel, PostModel


class UserOutput(BaseModel):

    id: UUID
    name: str
    username: str
    created_at: datetime

    # this method will receive an user model and filter fields that are not meant to be displayed to user
    @classmethod
    def show(self, data: UserModel):
        return UserOutput(id=data.id, name=data.name, username=data.username, created_at=data.created_at)

class JWTOutput(BaseModel):

    access: str
    refresh: str



class UserUpdateOutput(BaseModel):

    user: UserOutput
    token: JWTOutput


class PostOutput(BaseModel):

    id: int

    user: UserOutput

    title: str

    content: str

    created_at: datetime


    @classmethod
    def show(self, data: PostModel, user: UserModel) -> "PostOutput":
        
        user = UserOutput.show(user)
        
        return PostOutput(
            id=data.id, 
            user=user, 
            title=data.title, 
            content=data.content, 
            created_at=data.created_at
        )