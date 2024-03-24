from sqlmodel import Field, SQLModel


class _PlayerBase(SQLModel):
    name: str = Field(min_length=3, max_length=25, index=True, unique=True)


class PlayerCreate(_PlayerBase):
    pass


class Player(_PlayerBase, table=True):
    id: int | None = Field(default=None, primary_key=True)
    games_played: int = Field(default=0)
    games_won: int = Field(default=0)


class PlayerRead(Player):
    id: int


class PlayerUpdate(_PlayerBase):
    pass
