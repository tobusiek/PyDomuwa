from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domuwa.database import Base

if TYPE_CHECKING:
    from domuwa.answer.model import Answer


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String, nullable=False, index=True)
    author: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    answers: Mapped[Answer] = relationship("Answer", back_populates="question", cascade="all, delete")
    excluded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
