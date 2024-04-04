import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from domuwa import database as db
from domuwa.models.db_models import Player

logger = logging.getLogger(__name__)


async def create_player(player: Player, db_sess: Session = Depends(db.get_db_session)):
    try:
        db_player = await db.save(player, db_sess)
    except IntegrityError as exc:
        logger.error(str(exc))
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Player of given name already exists"
        ) from exc
    return db_player


async def get_player_by_id(
    player_id: int, db_sess: Session = Depends(db.get_db_session)
):
    return await db.get(player_id, Player, db_sess)


async def get_player_by_name(
    player_name: str, db_sess: Session = Depends(db.get_db_session)
):
    db_player = db_sess.exec(select(Player).where(Player.name == player_name)).first()
    if db_player is None:
        err_msg = f"Player with name={player_name} not found"
        logger.error("")
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)
    return db_player


async def get_all_players(db_sess: Session = Depends(db.get_db_session)):
    return await db.get_all(Player, db_sess)


async def update_player(
    player_id: int, player: Player, db_sess: Session = Depends(db.get_db_session)
):
    return await db.update(player_id, player, db_sess)


async def delete_player(player_id: int, db_sess: Session = Depends(db.get_db_session)):
    await db.delete(player_id, Player, db_sess)
