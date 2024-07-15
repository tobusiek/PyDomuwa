from typing import Annotated

from fastapi import APIRouter, Depends

from domuwa.auth import get_current_user
from domuwa.auth.models import User

router = APIRouter(prefix="auth")


@router.get("")
async def read_user(current_user: Annotated[User, Depends(get_current_user)]):
    return current_user
