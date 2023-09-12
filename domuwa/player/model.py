from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domuwa.database import Base

if TYPE_CHECKING:
    from domuwa.game_room.model import GameRoom


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
    game_rooms_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    game_rooms_won: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    game_room_id: Mapped[int] = mapped_column(Integer, ForeignKey("game_room.id"), nullable=True)
    game_room: Mapped[GameRoom] = relationship("GameRoom", back_populates="players", foreign_keys=game_room_id)
