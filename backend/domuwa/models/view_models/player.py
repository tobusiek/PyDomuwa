from sqlmodel import Field, SQLModel


class PlayerBase(SQLModel):
    name: str = Field(min_length=3, max_length=25)


class PlayerCreate(PlayerBase):
    pass


class PlayerSession(PlayerBase):
    id: int


class PlayerRead(PlayerBase):
    id: int
    games_played: int
    games_won: int


class PlayerUpdate(PlayerBase):
    pass
