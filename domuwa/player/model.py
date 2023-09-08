from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from domuwa.database import Base

if TYPE_CHECKING:
    from domuwa.game.model import Game


class Player(Base):
    __tablename__ = "players"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False, index=True, unique=True)
    games_played: Mapped[int] = Column(Integer, nullable=False, default=0)
    games_won: Mapped[int] = Column(Integer, nullable=False, default=0)
    score: Mapped[float] = Column(Float, nullable=False, default=0.0)
    game_id: Mapped[int] = Column(Integer, ForeignKey("games.id"), nullable=True)
    game: Mapped[Game] = relationship("Game", back_populates="players", foreign_keys=game_id)
