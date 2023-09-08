from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from domuwa.database import Base

if TYPE_CHECKING:
    from domuwa.answer.model import Answer
    from domuwa.game.model import Game


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    game: Mapped[Game] = relationship("Game", back_populates="questions")
    game_name: Mapped[str] = Column(String, nullable=False, index=True)
    category: Mapped[str] = Column(String, nullable=False, index=True)
    author: Mapped[str] = Column(String, nullable=False)
    text: Mapped[str] = Column(String, nullable=False)
    answers: Mapped[Answer] = relationship("Answer", back_populates="question")
    correct_answer_id: Mapped[int] = Column(Integer, ForeignKey(column="answer.id"), nullable=True)
    excluded: Mapped[bool] = Column(Boolean, default=False, nullable=False)
