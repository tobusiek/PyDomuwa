from datetime import datetime
from enum import Enum as PyEnum
from typing import Optional

from sqlmodel import Column, Enum, Field, Relationship, SQLModel


class GameTypeChoices(PyEnum):
    EGO = "Ego"
    WHOS_MOST_LIKELY = "Who's Most Likely"
    GENTLEMENS_CARDS = "Gentlemen's cards"
    NEVER_HAVE_I_EVER = "Never have I ever"


class GameType(SQLModel, table=True):
    __tablename__ = "game_type"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: GameTypeChoices = Field(sa_column=Column(Enum(GameTypeChoices)))

    questions: list["Question"] = Relationship(back_populates="game_type")
    answers: list["Answer"] = Relationship(back_populates="game_type")
    game_rooms: list["GameRoom"] = Relationship(back_populates="game_type")


class QnACategoryChoices(PyEnum):
    SFW = "SFW"
    NSFW = "NSFW"


class QnACategory(SQLModel, table=True):
    __tablename__ = "qna_category"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: QnACategoryChoices = Field(sa_column=Column(Enum(QnACategoryChoices)))

    questions: list["Question"] = Relationship(back_populates="game_category")
    answers: list["Answer"] = Relationship(back_populates="game_category")


class Player(SQLModel, table=True):
    __tablename__ = "player"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: str = Field(min_length=3, max_length=25, index=True, unique=True)
    games_played: int = Field(default=0)
    games_won: int = Field(default=0)

    questions: list["Question"] = Relationship(back_populates="author")
    answers: list["Answer"] = Relationship(back_populates="author")

    game_room_id: Optional[int] = Field(
        default=None, foreign_key="game_room.id", nullable=True
    )
    game_room: Optional["GameRoom"] = Relationship(back_populates="players")


class Answer(SQLModel, table=True):
    __tablename__ = "answer"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(min_length=1, max_length=150)
    excluded: bool = Field(default=False, index=True)

    author_name: Optional[str] = Field(default=None, foreign_key="player.name")
    author: Optional[Player] = Relationship(back_populates="answers")

    game_type_id: Optional[int] = Field(default=None, foreign_key="game_type.id")
    game_type: Optional[GameType] = Relationship(back_populates="answers")

    game_category_id: Optional[int] = Field(default=None, foreign_key="qna_category.id")
    game_category: Optional[QnACategory] = Relationship(back_populates="answers")

    question_id: Optional[int] = Field(
        default=None, foreign_key="question.id", nullable=True
    )
    question: Optional["Question"] = Relationship(back_populates="answers")


class GameRoomQuestionsLink(SQLModel, table=True):
    game_room_id: Optional[int] = Field(
        default=None, foreign_key="game_room.id", primary_key=True
    )
    question_id: Optional[int] = Field(
        default=None, foreign_key="question.id", primary_key=True
    )

    game_room: "GameRoom" = Relationship(back_populates="question_links")
    question: "Question" = Relationship(back_populates="game_room_links")


class Question(SQLModel, table=True):
    __tablename__ = "question"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(min_length=3, max_length=150)
    excluded: bool = Field(default=False, index=True)

    author_name: Optional[str] = Field(default=None, foreign_key="player.name")
    author: Optional[Player] = Relationship(back_populates="questions")

    game_type_id: Optional[int] = Field(default=None, foreign_key="game_type.id")
    game_type: Optional[GameType] = Relationship(back_populates="questions")

    game_category_id: Optional[int] = Field(default=None, foreign_key="qna_category.id")
    game_category: Optional[QnACategory] = Relationship(back_populates="questions")

    answers: list[Answer] = Relationship(back_populates="question")

    game_room_links: GameRoomQuestionsLink = Relationship(back_populates="question")


class GameCategoryChoices(PyEnum):
    SFW = "SFW"
    NSFW = "NSFW"
    MIXED = "Mixed"


class GameCategory(SQLModel, table=True):
    __tablename__ = "game_category"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: GameCategoryChoices = Field(sa_column=Column(Enum(GameCategoryChoices)))

    game_rooms: list["GameRoom"] = Relationship(back_populates="game_category")


class GameRoom(SQLModel, table=True):
    __tablename__ = "game_room"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    websocket: Optional[str] = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    rounds: int = 15
    cur_round: int = 0

    game_type_id: Optional[int] = Field(default=None, foreign_key="game_type.id")
    game_type: Optional[GameType] = Relationship(back_populates="game_rooms")

    game_category_id: Optional[int] = Field(
        default=None, foreign_key="game_category.id"
    )
    game_category: Optional[GameCategory] = Relationship(back_populates="game_rooms")

    question_links: list[GameRoomQuestionsLink] = Relationship(
        back_populates="game_room"
    )

    players: list[Player] = Relationship(back_populates="game_room")

    ranking: Optional["Ranking"] = Relationship(back_populates="game_room")


class Ranking(SQLModel, table=True):
    __tablename__ = "ranking"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    game_room_id: Optional[int] = Field(default=None, foreign_key="game_room.id")
    game_room: Optional[GameRoom] = Relationship(back_populates="ranking")

    player_scores: list["PlayerScore"] = Relationship(back_populates="ranking")


class PlayerScore(SQLModel, table=True):
    __tablename__ = "player_score"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)

    ranking_id: Optional[int] = Field(default=None, foreign_key="ranking.id")
    ranking: Optional[Ranking] = Relationship(back_populates="player_scores")
