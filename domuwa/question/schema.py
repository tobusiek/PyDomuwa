from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from domuwa.answer.schema import AnswerView
    from domuwa.game.schema import GameView


class QuestionBase(BaseModel):
    game_name: str
    category: str
    author: str
    text: str
    correct_answer_id: Optional[int]
    excluded: bool


class QuestionCreate(QuestionBase):
    excluded: bool = False


class QuestionView(QuestionBase):
    id: int
    game: Optional[GameView]
    answers: list[AnswerView]
    model_config = ConfigDict(from_attributes=True)
