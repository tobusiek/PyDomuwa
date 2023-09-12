from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from domuwa.game_room.schema import GameRoomView


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class PlayerView(PlayerBase):
    id: int
    games_played: int
    games_won: int
    score: float
    model_config = ConfigDict(from_attributes=True)


class PlayerViewWithGame(PlayerView):
    game: Optional[GameRoomView]
