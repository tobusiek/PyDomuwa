from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from domuwa.models.game_room import GameRoom
    from domuwa.models.player_score import PlayerScore


class Ranking(SQLModel, table=True):
    __tablename__ = "ranking"  # type: ignore

    id: Optional[int] = Field(None, primary_key=True)

    game_room_id: Optional[int] = Field(None, foreign_key="game_room.id")
    game_room: Optional["GameRoom"] = Relationship(back_populates="ranking")

    player_scores: list["PlayerScore"] = Relationship(back_populates="ranking")
