from fastapi.exceptions import HTTPException
from fastapi import status


class NotFoundException(HTTPException):

    def __init__(self, model_name):
        self.status_code = status.HTTP_404_NOT_FOUND

        self.detail = f"the given request not found on {model_name} table"



class DuplicateException(HTTPException):

    def __init__(self, model_name):
        self.status_code = status.HTTP_409_CONFLICT

        self.detail = f"the given credentials is already on {model_name} table"



class UsernameOrPasswordException(HTTPException):
    
    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST

        self.detail = "the give username or password is wrong" 




class InvalideTokenException(HTTPException):

    def __init__(self, message: str):
        self.status_code = status.HTTP_400_BAD_REQUEST

        self.detail = message


class NoFieldWerePassed(HTTPException):

    def __init__(self):
        self.status_code = status.HTTP_400_BAD_REQUEST

        self.detail = "no fields were passed to be processed"