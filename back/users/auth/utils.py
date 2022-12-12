from jwt import decode, encode
from users.crud import UserCRUD
from .exceptions import TokenException

SECRETKEY = "some really specific stuff"



def generate_token(payload) -> str:
    token = encode(payload={"email": payload}, key=SECRETKEY,  algorithm='HS256')
    return token


def get_email(token): 
    payload = decode(jwt=token, key=SECRETKEY, algorithms=['HS256'])
    return payload["email"]


async def is_auth(token: str, db):
    email = get_email(token)
    user = await UserCRUD(db).get_user_by_email(email=email)
    if user is None:
        raise TokenException
    return user
