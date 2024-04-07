from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from domuwa.models.answer import Answer
    from domuwa.models.game_room import GameRoom
    from domuwa.models.question import Question


class GameTypeChoices(StrEnum):
    EGO = "Ego"
    WHOS_MOST_LIKELY = "Who's Most Likely"
    GENTLEMENS_CARDS = "Gentlemen's cards"
    NEVER_HAVE_I_EVER = "Never have I ever"


class GameTypeBase(SQLModel):
    name: GameTypeChoices


class GameType(SQLModel, table=True):
    __tablename__ = "game_type"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: GameTypeChoices = Field(index=True, unique=True)

    questions: list["Question"] = Relationship(back_populates="game_type")
    answers: list["Answer"] = Relationship(back_populates="game_type")
    game_rooms: list["GameRoom"] = Relationship(back_populates="game_type")


class GameTypeCreate(GameTypeBase):
    pass


class GameTypeRead(GameTypeBase):
    id: int


class GameTypeUpdate(GameTypeBase):
    pass
