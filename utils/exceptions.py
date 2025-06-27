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