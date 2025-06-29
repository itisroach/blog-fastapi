from pydantic import BaseModel, Field
from typing import Optional

class UserInput(BaseModel):

    name: Optional[str] = "Unknown"

    username: str = Field(min_length=3, max_length=32)
    
    password: str = Field(min_length=8, max_length=64)


class UserLoginInput(BaseModel):

    username: str
    password: str
    

class UpdateUserInput(BaseModel):

    username: Optional[str] = Field(min_length=3, max_length=32, default=None)
    name: Optional[str] = Field(min_length=3, max_length=32, default=None)


class UserRefreshTokenInput(BaseModel):

    token: str


class PostInput(BaseModel):

    title: str = Field(min_length=10, max_length=128)

    content: str = Field(min_length=128, max_length=1024)

    username: str

