from __future__ import annotations

from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from domuwa.question.schema import QuestionView


class AnswerBase(BaseModel):
    author: str
    text: str
    points: float
    question_id: int


class AnswerCreate(AnswerBase):
    pass


class AnswerView(AnswerBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class AnswerViewWithQuestion(AnswerView):
    question: QuestionView
