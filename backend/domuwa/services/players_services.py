import logging

from fastapi import Depends, HTTPException, status
from pydantic import ValidationError
from sqlmodel import Session, select

from domuwa import database as db
from domuwa.models.db_models import Player
from domuwa.models.view_models.player import PlayerCreate, PlayerUpdate

logger = logging.getLogger(__name__)


async def create_player(
    player_create: PlayerCreate, db_sess: Session = Depends(db.get_db_session)
):
    try:
        player = Player.model_validate(player_create, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Provided invalid data",
        ) from exc

    return await db.save(player, db_sess)


async def get_player_by_id(
    player_id: int,
    db_sess: Session = Depends(db.get_db_session),
):
    return await db.get(player_id, Player, db_sess)


async def get_player_by_name(
    player_name: str,
    db_sess: Session = Depends(db.get_db_session),
):
    db_player = db_sess.exec(select(Player).where(Player.name == player_name)).first()
    if db_player is None:
        err_msg = f"Player with name={player_name} not found"
        logger.error(err_msg)
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)
    return db_player


async def get_all_players(db_sess: Session = Depends(db.get_db_session)):
    return await db.get_all(Player, db_sess)


async def update_player(
    player_id: int,
    player_update: PlayerUpdate,
    db_sess: Session = Depends(db.get_db_session),
):
    try:
        player = Player.model_validate(player_update, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Provided invalid data",
        ) from exc
    return await db.update(player_id, player, db_sess)


async def delete_player(player_id: int, db_sess: Session = Depends(db.get_db_session)):
    await db.delete(player_id, Player, db_sess)
