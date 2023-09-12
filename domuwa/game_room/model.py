from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from domuwa.database import Base

if TYPE_CHECKING:
    from domuwa.player.model import Player


class GameRoom(Base):
    __tablename__ = "games"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    game_name: Mapped[str] = Column(String, nullable=False)
    game_category: Mapped[str] = Column(String, nullable=False)
    players: Mapped[list[Player]] = relationship("Player", back_populates="game_room")
