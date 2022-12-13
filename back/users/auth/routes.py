from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer 


scheme = OAuth2PasswordBearer(tokenUrl="/token")
