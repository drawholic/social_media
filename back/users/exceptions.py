from fastapi import HTTPException


class PasswordsDoNotMatch(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Given passwords do not match")


class UserAlreadyExists(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User already exists")


class UserDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="User does not exists")