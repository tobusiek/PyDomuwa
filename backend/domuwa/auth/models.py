from pydantic import BaseModel
from sqlmodel import Field, SQLModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    username: str


class User(SQLModel):
    login: str
    email: str | None = None
    is_active: bool | None = None
    is_staff: bool | None = None


class UserDb(User, table=True):
    # TODO: add admin privileges
    __tablename__ = "user"

    id: int | None = Field(None, primary_key=True)
    hashed_password: str
