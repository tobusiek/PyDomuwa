from datetime import datetime
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from domuwa.models.links import GameRoomQuestionsLink

if TYPE_CHECKING:
    from domuwa.models.game_category import GameCategory
    from domuwa.models.game_type import GameType
    from domuwa.models.player import Player
    from domuwa.models.question import Question
    from domuwa.models.ranking import Ranking


class GameRoom(SQLModel, table=True):
    __tablename__ = "game_room"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    websocket: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    rounds: int = 15
    cur_round: int = 0

    game_type_id: Optional[int] = Field(default=None, foreign_key="game_type.id")
    game_type: Optional["GameType"] = Relationship(back_populates="game_rooms")

    game_category_id: Optional[int] = Field(
        default=None,
        foreign_key="game_category.id",
    )
    game_category: Optional["GameCategory"] = Relationship(back_populates="game_rooms")

    questions: list["Question"] = Relationship(
        back_populates="game_rooms",
        link_model=GameRoomQuestionsLink,
    )

    players: list["Player"] = Relationship(back_populates="game_room")

    ranking: Optional["Ranking"] = Relationship(back_populates="game_room")
