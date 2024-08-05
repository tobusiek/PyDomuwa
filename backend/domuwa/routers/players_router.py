import logging

from fastapi import APIRouter, Depends
from sqlmodel import Session
from typing_extensions import override

from domuwa.database import get_db_session
from domuwa.models.player import (
    Player,
    PlayerCreate,
    PlayerRead,
    PlayerUpdate,
)
from domuwa.routers.common_router import CommonRouter400OnSaveError
from domuwa.services.players_services import PlayerServices


class PlayerRouter(CommonRouter400OnSaveError[PlayerCreate, PlayerUpdate, Player]):
    prefix = "/players"
    tags = ["Player"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = PlayerRead
    services = PlayerServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = Player.__name__

    @override
    async def create(self, model: PlayerCreate, session: Session = Depends(get_db_session)):
        return await super().create(model, session)

    @override
    async def update(self, model_id: int, model_update: PlayerUpdate, session: Session = Depends(get_db_session)):
        return await super().update(model_id, model_update, session)


def get_players_router():
    return PlayerRouter().router
