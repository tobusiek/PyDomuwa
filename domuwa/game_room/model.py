from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domuwa.database import Base

if TYPE_CHECKING:
    from domuwa.player.model import Player


class GameRoom(Base):
    __tablename__ = "game_room"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_name: Mapped[str] = mapped_column(String, nullable=False)
    game_category: Mapped[str] = mapped_column(String, nullable=False)
    players: Mapped[list[Player]] = relationship("Player", back_populates="game_room")
