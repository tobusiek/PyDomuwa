from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, relationship

from domuwa.database import Base

if TYPE_CHECKING:
    from domuwa.question.model import Question


class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    author: Mapped[str] = Column(String, nullable=False)
    text: Mapped[str] = Column(String, nullable=False)
    points: Mapped[float] = Column(Float, nullable=True, default=0.0)
    question_id: Mapped[int] = Column(Integer, ForeignKey(column="question.id", ondelete="CASCADE"))
    question: Mapped[Question] = relationship("Question", back_populates="answers")
