import logging

from fastapi import APIRouter, Depends, status
from sqlmodel import Session

from domuwa.database import get_db_session
from domuwa.models.view_models.player import PlayerCreate, PlayerRead, PlayerUpdate
from domuwa.services import players_services as services

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", response_model=PlayerRead, status_code=status.HTTP_201_CREATED)
async def create_player(
    player: PlayerCreate,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug(f"received Player({player}) to create")
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


@router.patch("/{player_id}", response_model=PlayerRead)
async def update_player(
    player_id: int,
    player: PlayerUpdate,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug(f"received Player({player}) to update Player(id={player_id})")
    return await services.update_player(player_id, player, db_sess)


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_id: int, db_sess: Session = Depends(get_db_session)):
    logger.debug(f"received Player(id={player_id}) to remove")
    await services.delete_player(player_id, db_sess)
