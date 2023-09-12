from __future__ import annotations

from enum import Enum
from typing import TYPE_CHECKING

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator

if TYPE_CHECKING:
    from domuwa.player.schema import PlayerView


class GameCategory(Enum):
    SFW = "SFW"
    NSFW = "NSFW"
    MIXED = "MIXED"


class GameRoomBase(BaseModel):
    game_name: str
    game_category: str

    @field_validator("game_category")
    @classmethod
    def check_category(cls, category: str) -> str:
        if category not in [game_cat.value for game_cat in GameCategory]:
            raise ValidationError(f"Invalid {category=}")
        return category


class GameRoomCreate(GameRoomBase):
    ...


class GameRoomView(GameRoomBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class GameViewWithPlayers(GameRoomView):
    players: list[PlayerView]
