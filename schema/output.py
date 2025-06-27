from pydantic import BaseModel
from uuid import UUID


class UserOutput(BaseModel):

    id: UUID
    name: str
    username: str


class JWTOutput(BaseModel):

    access: str
    refresh: str