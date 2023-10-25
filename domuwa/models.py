from __future__ import annotations

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
    question_id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey(column="question.id", ondelete="CASCADE"),
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


class Player(Base):
    __tablename__ = "player"

    id: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer,
        primary_key=True,
        autoincrement=True,
    )
    name: orm.Mapped[str] = orm.mapped_column(
        sqlalchemy.String,
        nullable=False,
        index=True,
        unique=True,
    )
    game_rooms_played: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer,
        nullable=False,
        default=0,
    )
    game_rooms_won: orm.Mapped[int] = orm.mapped_column(
        sqlalchemy.Integer,
        nullable=False,
        default=0,
    )
    score: orm.Mapped[float] = orm.mapped_column(
        sqlalchemy.Float,
        nullable=False,
        default=0.0,
    )
    game_room_id: orm.Mapped[int | None] = orm.mapped_column(
        sqlalchemy.Integer,
        sqlalchemy.ForeignKey("game_room.id"),
        nullable=True,
    )
    game_room: orm.Mapped[GameRoom | None] = orm.relationship(
        "GameRoom",
        back_populates="players",
        foreign_keys=game_room_id,
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
