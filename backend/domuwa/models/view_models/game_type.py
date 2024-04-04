from pydantic import BaseModel

from domuwa.models.db_models import GameTypeChoices


class GameTypeBase(BaseModel):
    name: GameTypeChoices


class GameTypeCreate(GameTypeBase):
    pass


class GameTypeRead(GameTypeBase):
    id: int


class GameTypeUpdate(GameTypeBase):
    pass
