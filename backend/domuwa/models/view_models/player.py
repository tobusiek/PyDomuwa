from domuwa.models.db_models import DbPlayer
from sqlmodel import Field, SQLModel


class Player(SQLModel):
    name: str = Field(min_length=3, max_length=25)


class PlayerSession(Player):
    id: int


class PlayerRead(DbPlayer):
    id: int


class PlayerUpdate(Player):
    pass
