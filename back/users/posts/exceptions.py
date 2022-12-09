from fastapi import HTTPException


class PostDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Post does not exist")