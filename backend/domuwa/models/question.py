from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from domuwa.models.links import GameRoomQuestionsLink

if TYPE_CHECKING:
    from domuwa.models.answer import Answer, AnswerRead
    from domuwa.models.game_room import GameRoom
    from domuwa.models.game_type import GameType, GameTypeRead
    from domuwa.models.player import Player, PlayerRead
    from domuwa.models.qna_category import QnACategory, QnACategoryRead

TEXT_MIN_LEN = 3
TEXT_MAX_LEN = 250


class QuestionBase(SQLModel):
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool = False
    author_id: int
    game_type_id: int
    game_category_id: int


class Question(SQLModel, table=True):
    __tablename__ = "question"  # type: ignore

    id: Optional[int] = Field(None, primary_key=True)
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool = Field(False, index=True)
    deleted: bool = Field(False, index=True)

    author_id: Optional[int] = Field(None, foreign_key="player.id")
    author: Optional["Player"] = Relationship(back_populates="questions")

    game_type_id: Optional[int] = Field(None, foreign_key="game_type.id")
    game_type: Optional["GameType"] = Relationship(back_populates="questions")

    game_category_id: Optional[int] = Field(None, foreign_key="qna_category.id")
    game_category: Optional["QnACategory"] = Relationship(back_populates="questions")

    prev_version_id: Optional[int] = Field(None, foreign_key="question.id")
    prev_version: Optional["Question"] = Relationship(
        back_populates="next_versions",
        sa_relationship_kwargs={"remote_side": "Question.id"},
    )
    next_versions: list["Question"] = Relationship(back_populates="prev_version")

    answers: list["Answer"] = Relationship(back_populates="question")

    game_rooms: list["GameRoom"] = Relationship(
        back_populates="questions",
        link_model=GameRoomQuestionsLink,
    )


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(SQLModel):
    pass


class QuestionRead(SQLModel):
    id: int
    text: str = Field(min_length=TEXT_MIN_LEN, max_length=TEXT_MAX_LEN)
    excluded: bool = False
    author: "PlayerRead"
    game_type: "GameTypeRead"
    game_category: "QnACategoryRead"


class QuestionWithAnswersRead(QuestionRead):
    answers: list["AnswerRead"]
