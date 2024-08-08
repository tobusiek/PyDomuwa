from sqlmodel import Field, SQLModel


class Token(SQLModel):
    access_token: str
    token_type: str


class TokenData(SQLModel):
    username: str


class User(SQLModel, table=True):
    login: str
    email: str | None = None


class UserDb(User, table=True):
    # TODO: add admin privileges

    id: int | None = Field(None, primary_key=True)
    hashed_password: str
