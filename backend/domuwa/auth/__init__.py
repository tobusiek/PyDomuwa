# Add Fb/Google authorization: https://fastapi.tiangolo.com/advanced/security/oauth2-scopes/#global-view

from datetime import datetime, timedelta, timezone
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from passlib.context import CryptContext
from sqlmodel import Session

from domuwa.auth import services
from domuwa.auth.models import TokenData, User
from domuwa.config import settings
from domuwa.database import get_db_session

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

CredentialsException = HTTPException(
    status.HTTP_401_UNAUTHORIZED,
    detail="Could not validate credentials",
    headers={"WWW-Authenticate": "Bearer"},
)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def authenticate_user(username: str, password: str, session: Session):
    user = services.get_user(username, session)
    if user is None:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: timedelta | None = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.HASH_ALGORITHM)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    session: Annotated[Session, Depends(get_db_session)],
):
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.HASH_ALGORITHM]
        )
    except jwt.InvalidTokenError:
        raise CredentialsException

    username: str = payload.get("sub")
    if username is None:
        raise CredentialsException

    token_data = TokenData(username=username)
    user = services.get_user(token_data.username, session)
    if user is None:
        raise CredentialsException
    return user


async def get_current_active_user(current_user: User = Depends(get_current_user)):
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Inactive user"
        )
