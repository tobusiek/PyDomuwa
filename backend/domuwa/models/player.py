from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from domuwa.models.answer import Answer
    from domuwa.models.game_room import GameRoom
    from domuwa.models.player_score import PlayerScore
    from domuwa.models.question import Question


class PlayerBase(SQLModel):
    name: str = Field(min_length=3, max_length=25)


class Player(SQLModel, table=True):
    __tablename__ = "player"  # type: ignore

    id: Optional[int] = Field(None, primary_key=True)
    name: str = Field(min_length=3, max_length=25, index=True, unique=True)
    games_played: int = 0
    games_won: int = 0

    questions: list["Question"] = Relationship(back_populates="author")
    answers: list["Answer"] = Relationship(back_populates="author")

    game_room_id: Optional[int] = Field(None, foreign_key="game_room.id", nullable=True)
    game_room: Optional["GameRoom"] = Relationship(back_populates="players")

    player_scores: list["PlayerScore"] = Relationship(back_populates="player")


class PlayerCreate(PlayerBase):
    pass


class PlayerLogin(PlayerBase):
    pass


class PlayerSession(PlayerBase):
    id: int


class PlayerRead(PlayerSession):
    games_played: int
    games_won: int


class PlayerUpdate(PlayerBase):
    pass
