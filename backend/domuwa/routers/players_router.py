import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing_extensions import override

from domuwa.database import get_db_session
from domuwa.models.player import (
    Player,
    PlayerCreate,
    PlayerRead,
    PlayerUpdate,
)
from domuwa.routers.common_router import CommonRouter
from domuwa.services.players_services import PlayerServices


class PlayerRouter(CommonRouter[PlayerCreate, PlayerUpdate, Player]):
    prefix = "/players"
    tags = ["Player"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = PlayerRead
    services = PlayerServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = Player.__name__

    @override
    async def create(
        self,
        create_model: PlayerCreate,
        session: Session = Depends(get_db_session),
    ):
        player = await super().create(create_model, session)
        if player is None:
            err_msg = f"Cannot create Player({create_model})."
            self.logger.warning(err_msg)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, err_msg)
        return player

    @override
    async def update(
        self,
        model_id: int,
        model_update: PlayerUpdate,
        session: Session = Depends(get_db_session),
    ):
        return await super().update(model_id, model_update, session)


def get_players_router():
    return PlayerRouter().router
