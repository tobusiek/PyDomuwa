from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Integer, String
from sqlalchemy.orm import Mapped, relationship

from domuwa.database import Base

if TYPE_CHECKING:
    from domuwa.answer.model import Answer


class Question(Base):
    __tablename__ = "questions"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    game_name: Mapped[str] = Column(String, nullable=False, index=True)
    category: Mapped[str] = Column(String, nullable=False, index=True)
    author: Mapped[str] = Column(String, nullable=False)
    text: Mapped[str] = Column(String, nullable=False)
    answers: Mapped[Answer] = relationship("Answer", back_populates="question", cascade="all, delete")
    excluded: Mapped[bool] = Column(Boolean, default=False, nullable=False)
