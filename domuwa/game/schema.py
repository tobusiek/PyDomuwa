from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, field_validator

if TYPE_CHECKING:
    from domuwa.player.schema import PlayerView
    from domuwa.question.schema import QuestionView


class GameCategory(Enum):
    SFW = "SFW"
    NSFW = "NSFW"
    MIXED = "MIXED"


class GameBase(BaseModel):
    name: str
    category: str

    @field_validator("category")
    @classmethod
    def check_category(cls, category: str) -> str:
        assert category in (game_cat.value for game_cat in GameCategory)
        return category


class GameCreate(GameBase):
    ...


class GameView(GameBase):
    id: int
    questions: list[QuestionView]
    model_config = ConfigDict(from_attributes=True)


class GameViewWithPlayers(GameView):
    players: list[PlayerView]
