import logging

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing_extensions import override

from domuwa.database import get_db_session
from domuwa.models.game_type import (
    GameType,
    GameTypeCreate,
    GameTypeRead,
    GameTypeUpdate,
)
from domuwa.routers.common_router import CommonRouter
from domuwa.services.game_type_services import GameTypeServices

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/game-types", tags=["Game Types"])


class GameTypeRouter(CommonRouter[GameTypeCreate, GameTypeUpdate, GameType]):
    prefix = "/game-types"
    tags = ["Game Type"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = GameTypeRead
    services = GameTypeServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = GameType.__name__

    def __init__(self) -> None:
        super().__init__()

    @override
    async def create(
        self,
        create_model: GameTypeCreate,
        session: Session = Depends(get_db_session),
    ):
        return await super().create(create_model, session)

    # TODO: add auth user
    @override
    async def update(
        self,
        model_id: int,
        model_update: GameTypeUpdate,
        session: Session = Depends(get_db_session),
    ):
        return await super().update(model_id, model_update, session)

    # TODO: add auth user
    @override
    async def delete(self, model_id: int, session: Session = Depends(get_db_session)):
        return await super().delete(model_id, session)


def get_game_types_router():
    return GameTypeRouter().router
