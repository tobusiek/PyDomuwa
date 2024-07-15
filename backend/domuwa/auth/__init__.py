from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer

from domuwa.auth.models import User

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")


def decode_token(token: str):
    return User(id=0, login=token + "decoded", hashed_password="f4k3pwd")


async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)]):
    return decode_token(token)
