from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session, select

from domuwa import database as db
from domuwa.models.db_models import Player


def create_player(
    player: Player,
    db_sess: Session = Depends(db.get_db_session),
):
    try:
        db_player = db.save_obj(player, db_sess)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Player of given name already exists",
        )
    return db_player


def get_player_by_id(player_id: int, db_sess: Session = Depends(db.get_db_session)):
    return db.get_obj_of_type_by_id(player_id, Player, "Player", db_sess)


def get_player_by_name(player_name: str, db_sess: Session = Depends(db.get_db_session)):
    db_player = db_sess.exec(select(Player).where(Player.name == player_name)).first()
    if db_player is None:
        raise HTTPException(
            status.HTTP_404_NOT_FOUND, f"Player of given name={player_name} not found"
        )
    return db_player


def get_all_players(db_sess: Session = Depends(db.get_db_session)):
    return db.get_all_objs_of_type(Player, db_sess)


def update_player_name(
    player_id: int,
    player: Player,
    db_sess: Session = Depends(db.get_db_session),
):
    return db.update_obj(player_id, player, "Player", db_sess)


def delete_player(player_id: int, db_sess: Session = Depends(db.get_db_session)):
    db.delete_obj(player_id, Player, "Player", db_sess)
