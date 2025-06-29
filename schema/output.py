from pydantic import BaseModel
from uuid import UUID
from db import UserModel


class UserOutput(BaseModel):

    id: UUID
    name: str
    username: str

    # this method will receive an user model and filter fields that are not meant to be displayed to user
    @classmethod
    def show(self, data: UserModel):
        return UserOutput(id=data.id, name=data.name, username=data.username)

class JWTOutput(BaseModel):

    access: str
    refresh: str



class UserUpdateOutput(BaseModel):

    user: UserOutput
    token: JWTOutput