from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from domuwa.models.player import Player
    from domuwa.models.ranking import Ranking


class PlayerScore(SQLModel, table=True):
    __tablename__ = "player_score"  # type: ignore

    id: Optional[int] = Field(None, primary_key=True)

    player_id: Optional[int] = Field(None, foreign_key="player.id")
    player: Optional["Player"] = Relationship(back_populates="player_scores")

    ranking_id: Optional[int] = Field(None, foreign_key="ranking.id")
    ranking: Optional["Ranking"] = Relationship(back_populates="player_scores")
