from __future__ import annotations

from typing import Optional

import sqlalchemy
from sqlalchemy import orm

from domuwa import database


class Base(orm.DeclarativeBase):
    __abstract__ = True


class Answer(Base):
    __tablename__ = "answer"

    id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )
    author: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, nullable=False)
    text: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, nullable=False)
    correct: orm.Mapped[bool] = orm.mapped_column(sqlalchemy.Boolean, nullable=True)
    question_id: orm.Mapped[Optional[int]] = orm.mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(column="question.id", ondelete="CASCADE"),
        nullable=True,
    )
    question: orm.Mapped[Question] = orm.relationship(
        "Question",
        back_populates="answers",
        foreign_keys=question_id,
    )

    def __repr__(self) -> str:
        return (
            f"Answer(id={self.id}, author={self.author}, text={self.text}, correct={self.correct}, "
            f"question_id={self.question_id})"
        )


class GameRoom(Base):
    __tablename__ = "game_room"

    id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )
    game_name: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, nullable=False)
    game_category: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String,
        nullable=False,
    )
    players: orm.Mapped[list[Player]] = orm.relationship(
        "Player",
        back_populates="game_room",
    )


class Question(Base):
    __tablename__ = "question"

    id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )
    game_name: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String,
        nullable=False,
        index=True,
    )
    category: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String,
        nullable=False,
        index=True,
    )
    author: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, nullable=False)
    text: orm.Mapped[str] = orm.mapped_column(sqlalchemy.String, nullable=False)
    answers: orm.Mapped[list[Answer]] = orm.relationship(
        "Answer",
        back_populates="question",
        cascade="all, delete",
    )
    excluded: orm.Mapped[bool] = orm.mapped_column(
        sqlalchemy.Boolean,
        default=False,
        nullable=False,
    )

    def __repr__(self) -> str:
        return (
            f"Question(id={self.id}, game={self.game_name}, category={self.category}, author={self.author}, "
            f"text={self.text}, excluded={self.excluded})"
        )


Base.metadata.create_all(database.engine)
