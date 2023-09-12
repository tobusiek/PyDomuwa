from __future__ import annotations

from sqlalchemy import Boolean, Float, ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from domuwa.database import Base


class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    author: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    correct: Mapped[bool] = mapped_column(Boolean, nullable=True)
    question_id: Mapped[int] = mapped_column(Integer, ForeignKey(column="question.id", ondelete="CASCADE"))
    question: Mapped[Question] = relationship("Question", back_populates="answers", foreign_keys=question_id)


class GameRoom(Base):
    __tablename__ = "game_room"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_name: Mapped[str] = mapped_column(String, nullable=False)
    game_category: Mapped[str] = mapped_column(String, nullable=False)
    players: Mapped[list[Player]] = relationship("Player", back_populates="game_room")


class Player(Base):
    __tablename__ = "player"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    name: Mapped[str] = mapped_column(String, nullable=False, index=True, unique=True)
    game_rooms_played: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    game_rooms_won: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    score: Mapped[float] = mapped_column(Float, nullable=False, default=0.0)
    game_room_id: Mapped[int] = mapped_column(Integer, ForeignKey("game_room.id"), nullable=True)
    game_room: Mapped[GameRoom] = relationship("GameRoom", back_populates="players", foreign_keys=game_room_id)


class Question(Base):
    __tablename__ = "question"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    game_name: Mapped[str] = mapped_column(String, nullable=False, index=True)
    category: Mapped[str] = mapped_column(String, nullable=False, index=True)
    author: Mapped[str] = mapped_column(String, nullable=False)
    text: Mapped[str] = mapped_column(String, nullable=False)
    answers: Mapped[Answer] = relationship("Answer", back_populates="question", cascade="all, delete")
    excluded: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
