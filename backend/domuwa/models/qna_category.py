from enum import StrEnum
from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

if TYPE_CHECKING:
    from domuwa.models.answer import Answer
    from domuwa.models.question import Question


class QnACategoryChoices(StrEnum):
    SFW = "SFW"
    NSFW = "NSFW"


class QnACategoryBase(SQLModel):
    name: QnACategoryChoices


class QnACategory(SQLModel, table=True):
    __tablename__ = "qna_category"  # type: ignore

    id: Optional[int] = Field(default=None, primary_key=True)
    name: QnACategoryChoices = Field(index=True, unique=True)

    questions: list["Question"] = Relationship(back_populates="game_category")
    answers: list["Answer"] = Relationship(back_populates="game_category")


class QnACategoryCreate(QnACategoryBase):
    pass


class QnACategoryRead(QnACategoryBase):
    id: int


class QnACategoryUpdate(QnACategoryBase):
    pass
