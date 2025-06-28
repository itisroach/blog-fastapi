from pydantic import BaseModel, Field
from typing import Optional

class UserInput(BaseModel):

    name: Optional[str] = "Unknown"

    username: str = Field(min_length=3, max_length=32)
    
    password: str = Field(min_length=8, max_length=64)


class UserLoginInput(BaseModel):

    username: str
    password: str


class UserRefreshTokenInput(BaseModel):

    token: str