import logging

from fastapi import APIRouter, Depends, HTTPException, status
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
        model: GameTypeCreate,
        session: Session = Depends(get_db_session),
    ):
        game_type = await super().create(model, session)
        if game_type is None:
            err_msg = f"Cannot create GameType({model})."
            self.logger.warning(err_msg)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, err_msg)
        return game_type

    # TODO: add auth user
    # noinspection DuplicatedCode
    @override
    async def update(
        self,
        model_id: int,
        model_update: GameTypeUpdate,
        session: Session = Depends(get_db_session),
    ):
        db_game_type = await self.get_instance(model_id, session)
        game_type_update = await self.services.update(db_game_type, model_update, session)
        if game_type_update is None:
            err_msg = f"Cannot update GameType(id={model_id}) with GameType({model_id})."
            self.logger.warning(err_msg)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, err_msg)
        return game_type_update

    # TODO: add auth user
    @override
    async def delete(self, model_id: int, session: Session = Depends(get_db_session)):
        return await super().delete(model_id, session)


def get_game_types_router():
    return GameTypeRouter().router
