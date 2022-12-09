from jwt import decode, encode

SECRETKEY = "some really specific stuff"



def generate_token(payload) -> str:
    token = encode(payload={"email": payload}, key=SECRETKEY,  algorithm='HS256')
    return token


def get_email(token):
    payload = decode(jwt=token, key=SECRETKEY, algorithms=['HS256'])
    return payload["email"]
