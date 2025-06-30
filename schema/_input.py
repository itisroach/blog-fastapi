from pydantic import BaseModel, Field, field_validator
from typing import Optional
import re

# a class to inherit from for checking if any field is empty or just white
class NoWhiteSpace:

    __strip_fields__: tuple[str, ...] = ()


    @field_validator("*", mode="before")
    def remove_white_space(cls, value, field):

        if field.field_name in cls.__strip_fields__:

            if not isinstance(value, str):
                raise TypeError(f"{field.field_name} must be a string")
            
            if not value.strip():
                raise ValueError(f"{field.field_name} cannot be empty or only whitespace")

            return value.strip()
        
        return value
    
# a class to inherit from for checking if username contains white space in between and turn them to lowercase 
class NormalizeUsername:

    @field_validator("*", mode="before")
    def normalize_username(cls, value, field):

        if field.field_name == "username":
            if not isinstance(value, str):
                raise TypeError(f"{field.field_name} must be a string")
            
            if re.search(r'\s', value):
                raise ValueError('username must not contain whitespace characters')
        
        return value.lower().strip()
    


class UserInput(BaseModel, NoWhiteSpace, NormalizeUsername):

    name: Optional[str] = "Unknown"

    username: str = Field(min_length=3, max_length=32)
    
    password: str = Field(min_length=8, max_length=64)

    __strip_fields__ = ("name", "username", "password")


class UserLoginInput(BaseModel, NoWhiteSpace, NormalizeUsername):

    username: str
    password: str

    __strip_fields__ = ("username", "password")
    

class UpdateUserInput(BaseModel, NoWhiteSpace, NormalizeUsername):

    username: Optional[str] = Field(min_length=3, max_length=32, default=None)
    name: Optional[str] = Field(min_length=3, max_length=32, default=None)

    __strip_fields__ = ("name", "username")



class UserRefreshTokenInput(BaseModel):

    token: str


class PostInput(BaseModel, NoWhiteSpace):

    title: str = Field(min_length=10, max_length=128)

    content: str = Field(min_length=128, max_length=1024)

    __strip_fields__ = ("title", "content")


class PostUpdateInput(BaseModel, NoWhiteSpace):

    id: int

    title: Optional[str] = Field(min_length=10, max_length=128, default=None)

    content: Optional[str] = Field(min_length=128, max_length=1024, default=None)

    __strip_fields__ = ("title", "content")