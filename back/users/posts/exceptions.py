from fastapi import HTTPException


class PostDoesNotExist(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Post does not exist")


class PostAlreadyLiked(HTTPException):
    def __init__(self):
        super().__init__(status_code=400, detail="Post already liked")


class PostNotLiked(HTTPException):
    def __init(self):
        super().__init__(status_code=400, detail="Post is not liked")


class PostForbidden(HTTPException):
    def __init(self):
        super().__init__(status_code=400, detail="Post changes is forbidden for the user")