import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlmodel import Session

from domuwa.database import get_db_session
from domuwa.models.db_models import Player
from domuwa.models.view_models.player import PlayerCreate, PlayerRead, PlayerUpdate
from domuwa.services import players_services as services

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", response_model=PlayerRead, status_code=status.HTTP_201_CREATED)
async def create_player(
    player_create: PlayerCreate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        logger.debug(f"received Player({player_create}) to create")
        player = Player.model_validate(player_create, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Provided invalid data",
        ) from exc
    return await services.create_player(player, db_sess)


@router.get("/{player_id}", response_model=PlayerRead)
async def get_player_by_id(player_id: int, db_sess: Session = Depends(get_db_session)):
    logger.debug(f"received Player(id={player_id}) to get")
    return await services.get_player_by_id(player_id, db_sess)


@router.get("/name/", response_model=PlayerRead)
async def get_player_by_name(
    player_name: str,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug(f"received Player(name={player_name}) to get")
    return await services.get_player_by_name(player_name, db_sess)


@router.get("/", response_model=list[PlayerRead])
async def get_all_players(db_sess: Session = Depends(get_db_session)):
    return await services.get_all_players(db_sess)


@router.put("/{player_id}", response_model=PlayerRead)
async def update_player(
    player_id: int,
    player_update: PlayerUpdate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        logger.debug(
            f"received Player({player_update}) to update Player(id={player_id})"
        )
        player = Player.model_validate(player_update, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Provided invalid data",
        ) from exc

    return await services.update_player(player_id, player, db_sess)


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_id: int, db_sess: Session = Depends(get_db_session)):
    logger.debug(f"received Player(id={player_id}) to remove")
    await services.delete_player(player_id, db_sess)
