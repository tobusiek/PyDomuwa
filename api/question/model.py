from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from api.answer.model import Answer
from api.database import Base
from api.game.model import Game


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    game: Mapped[Game] = relationship("Game", back_populates="questions")
    game_name: Mapped[str] = Column(String, nullable=False, index=True)
    category: Mapped[str] = Column(String, nullable=False, index=True)
    text: Mapped[str] = Column(String, nullable=False)
    answers: Mapped[Answer] = relationship("Answer", back_populates="question")
    correct_answer_id: Mapped[int] = Column(Integer, ForeignKey("answer", column="answer.id"))
