import logging

from fastapi import Depends
from sqlmodel import Session

from domuwa import database as db
from domuwa.models.db_models import GameType

logger = logging.getLogger(__name__)


async def create_game_type(
    game_type: GameType, db_sess: Session = Depends(db.get_db_session)
):
    return await db.save(game_type, db_sess)


async def get_game_type_by_id(
    game_type_id: int, db_sess: Session = Depends(db.get_db_session)
):
    return await db.get(game_type_id, GameType, db_sess)


async def get_all_game_types(db_sess: Session = Depends(db.get_db_session)):
    return await db.get_all(GameType, db_sess)


async def update_game_type(
    game_type_id: int,
    game_type: GameType,
    db_sess: Session = Depends(db.get_db_session),
):
    return await db.update(game_type_id, game_type, db_sess)


async def delete_game_type(
    game_type_id: int, db_sess: Session = Depends(db.get_db_session)
):
    await db.delete(game_type_id, GameType, db_sess)
