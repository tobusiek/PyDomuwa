from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from domuwa import database as db
from domuwa.models.db_models import GameType


async def create_game_type(
    game_type: GameType, db_sess: Session = Depends(db.get_db_session)
):
    try:
        db_game_type = await db.save_obj(game_type, db_sess)
    except IntegrityError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "GameType of given name already exists"
        ) from exc
    return db_game_type


async def get_game_type_by_id(
    game_type_id: int, db_sess: Session = Depends(db.get_db_session)
):
    return await db.get_obj_of_type_by_id(game_type_id, GameType, "GameType", db_sess)


async def get_all_game_types(db_sess: Session = Depends(db.get_db_session)):
    return await db.get_all_objs_of_type(GameType, db_sess)


async def update_game_type(
    game_type_id: int,
    game_type: GameType,
    db_sess: Session = Depends(db.get_db_session),
):
    return await db.update_obj(game_type_id, game_type, "GameType", db_sess)


async def delete_game_type(
    game_type_id: int, db_sess: Session = Depends(db.get_db_session)
):
    await db.delete_obj(game_type_id, GameType, "GameType", db_sess)
