from typing import Optional

from api.game.schema import GameView
from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class PlayerView(PlayerBase):
    id: int
    games_played: int
    games_won: int
    score: float
    game: Optional[GameView]

    class Config:
        from_attributes = True
