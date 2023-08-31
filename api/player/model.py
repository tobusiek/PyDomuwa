from sqlalchemy import Integer, Column, String, Float
from sqlalchemy.orm import Mapped, relationship

from api.database import Base
from api.game.model import Game


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False, index=True, unique=True)
    games_played: Mapped[int] = Column(Integer, nullable=False, default=0)
    games_won: Mapped[int] = Column(Integer, nullable=False, default=0)
    score: Mapped[float] = Column(Float, nullable=False, default=0.0)
    game: Mapped[Game] = relationship("Game", back_populates="game.id")
