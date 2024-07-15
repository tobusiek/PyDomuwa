from typing import Optional

from sqlmodel import Field, SQLModel


class User(SQLModel):
    # TODO: add admin privileges

    id: Optional[int] = Field(None, primary_key=True)
    login: str
    email: str | None = None
    hashed_password: str
