from datetime import datetime
from enum import Enum as PyEnum

from sqlmodel import Field, Relationship, SQLModel


class GameTypeChoices(PyEnum):
    EGO = "Ego"
    WHOS_MOST_LIKELY = "Who's Most Likely"
    GENTLEMENS_CARDS = "Gentlemen's cards"
    NEVER_HAVE_I_EVER = "Never have I ever"


class DbGameType(SQLModel, table=True):
    __tablename__ = "game_type"

    id: int | None = Field(default=None, primary_key=True)
    name: GameTypeChoices

    questions: list["DbQuestion"] = Relationship(back_populates="game_type")
    answers: list["DbAnswer"] = Relationship(back_populates="game_type")
    game_rooms: list["DbGameRoom"] = Relationship(back_populates="game_type")


class QnACategoryChoices(PyEnum):
    SFW = "SFW"
    NSFW = "NSFW"


class QnACategory(SQLModel, table=True):
    __tablename__ = "qna_category"

    id: int | None = Field(default=None, primary_key=True)
    name: QnACategoryChoices = Field(
        min_length=2,
        max_length=10,
    )


class DbPlayer(SQLModel, table=True):
    __tablename__ = "player"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(
        min_length=3, max_length=25, index=True, unique=True, nullable=False
    )
    games_played: int = Field(default=0)
    games_won: int = Field(default=0)

    questions: list["DbQuestion"] = Relationship(back_populates="author")
    answers: list["DbAnswer"] = Relationship(back_populates="author")

    game_room_id: list["DbGameRoom"] = Relationship(back_populates="players")
    game_room: list["DbGameRoom"] = Relationship(back_populates="players")


class DbAnswer(SQLModel, table=True):
    __tablename__ = "answer"

    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(min_length=1, max_length=150)
    excluded: bool = Field(default=False, index=True)

    author_name: str = Field(default=None, foreign_key="player.name")
    author: DbPlayer | None = Field(default=None, foreign_key="player.id")

    question_id: int | None = Field(default=None, foreign_key="question.id")
    questions: "DbQuestion" = Relationship(back_populates="answers")


class GameRoomQuestionsLink(SQLModel):
    game_room_id: int | None = Field(
        default=None, foreign_key="game_room.id", primary_key=True
    )
    question_id: int | None = Field(
        default=None, foreign_key="question.id", primary_key=True
    )

    game_room: "DbGameRoom" = Relationship(back_populates="game_room_links")
    question: "DbQuestion" = Relationship(back_populates="question_links")


class DbQuestion(SQLModel, table=True):
    __tablename__ = "question"

    id: int | None = Field(default=None, primary_key=True)
    text: str = Field(min_length=3, max_length=150)
    excluded: bool = Field(default=False, index=True)

    author_name: str = Field(default=None, foreign_key="player.name")
    author: DbPlayer = Relationship(back_populates="questions")

    game_type_id: int | None = Field(default=None, foreign_key="game_type.id")
    game_type: DbGameType = Relationship(back_populates="questions")

    game_category_id: int | None = Field(default=None, foreign_key="qna_category.id")
    game_category: QnACategory = Relationship(back_populates="questions")

    answers: list[DbAnswer] = Relationship(back_populates="question")

    game_room: GameRoomQuestionsLink = Relationship(back_populates="question")


class GameCategoryChoices(PyEnum):
    SFW = "SFW"
    NSFW = "NSFW"
    MIXED = "Mixed"


class DbGameCategory(SQLModel, table=True):
    __tablename__ = "game_category"

    id: int | None = Field(default=None, primary_key=True)
    name: QnACategoryChoices = Field(
        min_length=2,
        max_length=10,
    )

    game_rooms: list["DbGameRoom"] = Relationship(back_populates="game_category")


class DbGameRoom(SQLModel, table=True):
    __tablename__ = "game_room"

    id: int | None = Field(default=None, primary_key=True)
    websocket: str | None = Field(default=None, index=True)
    created_at: datetime = Field(default_factory=datetime.now)
    rounds: int = Field(default=15)
    cur_round: int = Field(default=0)

    game_type_id: int | None = Field(default=None, foreign_key="game_type.id")
    game_type: DbGameType = Relationship(back_populates="game_rooms")

    game_category_id: int | None = Field(default=None, foreign_key="game_category.id")
    game_category: DbGameCategory = Relationship(back_populates="game_rooms")

    question_links: list[GameRoomQuestionsLink] = Relationship(
        back_populates="game_rooms"
    )

    players: list[DbPlayer] = Relationship(back_populates="game_room")

    ranking: "DbRanking" = Relationship(back_populates="game_room")


class DbRanking(SQLModel, table=True):
    __tablename__ = "ranking"

    id: int | None = Field(default=None, primary_key=True)

    game_room_id: int | None = Field(default=None, foreign_key="game_room.id")
    game_room: DbGameRoom | None = Relationship(back_populates="ranking")

    player_scores: list["DbPlayerScore"] = Relationship(back_populates="ranking")


class DbPlayerScore(SQLModel, table=True):
    __tablename__ = "player_score"

    id: int | None = Field(default=None, primary_key=True)

    ranking_id: int | None = Field(default=None, foreign_key="ranking.id")
    ranking: DbRanking = Relationship(back_populates="player_scores")
