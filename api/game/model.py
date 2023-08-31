from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from api.database import Base
from api.player.model import Player
from api.question.model import Question


class Game(Base):
    __tablename__ = "game"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = Column(String, nullable=False)
    category: Mapped[str] = Column(String, nullable=False)
    questions: Mapped[Question] = relationship("Question", back_populates="game")
    players: Mapped[Player] = relationship("Player", back_populates="game")
