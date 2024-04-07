from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from domuwa.models.game_type import GameType
    from domuwa.models.player import Player
    from domuwa.models.qna_category import QnACategory
    from domuwa.models.question import Question


class Answer(SQLModel, table=True):
    __tablename__ = "answer"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    text: str = Field(min_length=1, max_length=150)
    excluded: bool = Field(default=False, index=True)

    prev_version_id: Optional[int] = Field(None, foreign_key="answer.id")
    prev_version: Optional["Answer"] = Relationship(
        back_populates="next_versions",
        sa_relationship_kwargs={"remote_side": "Answer.id"},
    )

    next_versions: list["Answer"] = Relationship(back_populates="prev_version")

    author_id: Optional[int] = Field(default=None, foreign_key="player.id")
    author: Optional["Player"] = Relationship(back_populates="answers")

    game_type_id: Optional[int] = Field(default=None, foreign_key="game_type.id")
    game_type: Optional["GameType"] = Relationship(back_populates="answers")

    game_category_id: Optional[int] = Field(default=None, foreign_key="qna_category.id")
    game_category: Optional["QnACategory"] = Relationship(back_populates="answers")

    question_id: Optional[int] = Field(
        default=None,
        foreign_key="question.id",
        nullable=True,
    )
    question: Optional["Question"] = Relationship(back_populates="answers")
