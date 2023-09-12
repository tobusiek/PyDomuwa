from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domuwa.database import Base

if TYPE_CHECKING:
    from domuwa.question.model import Question


class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    correct: Mapped[bool] = mapped_column(Boolean, nullable=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey(column="question.id", ondelete="CASCADE"))
    question: Mapped[Question] = relationship("Question", back_populates="answers", foreign_keys=question_id)
