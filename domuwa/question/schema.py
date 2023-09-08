from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from domuwa.answer.schema import AnswerView


class QuestionBase(BaseModel):
    game_name: str
    category: str
    author: str
    text: str
    excluded: bool


class QuestionCreate(QuestionBase):
    excluded: bool = False


class QuestionView(QuestionBase):
    id: int
    answers: list[AnswerView]
    model_config = ConfigDict(from_attributes=True)
