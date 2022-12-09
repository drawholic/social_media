from fastapi import HTTPException


class AuthException(HTTPException):

    def __init__(self):
        super().__init__(status_code=400, detail="Incorrect email or password")


class TokenException(HTTPException):

    def __init__(self):
        super().__init__(status_code=400, detail="Invalid token")