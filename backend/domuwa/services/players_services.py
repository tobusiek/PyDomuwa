from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from domuwa import database as db
from domuwa import schemas
from domuwa.models import GameRoom, Player


def create_player(
    player: schemas.PlayerCreateSchema,
    db_sess: Session = Depends(db.get_db_session),
) -> Player:
    db_player = Player(name=player.name)
    try:
        db_player = db.save_obj(db_player, db_sess)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Player of given name already exists",
        )
    return db_player


def get_all_players_from_game_room(
    game_room_id: int,
    db_sess: Session = Depends(db.get_db_session),
) -> list[Player]:
    return db_sess.query(Player).filter(Player.game_room_id == game_room_id).all()


def update_player_name(
    player_id: int,
    new_name_player: schemas.PlayerCreateSchema,
    db_sess: Session = Depends(db.get_db_session),
) -> Player:
    player = db.get_obj_of_type_by_id(player_id, Player, "Player", db_sess)
    player.name = new_name_player.name
    return db.save_obj(player, db_sess)


def update_player_score(
    player_id: int,
    points: float,
    db_sess: Session = Depends(db.get_db_session),
) -> Player:
    player = db.get_obj_of_type_by_id(player_id, Player, "Player", db_sess)
    player.score += points
    return db.save_obj(player, db_sess)


def reset_player_score(
    player_id: int,
    db_sess: Session = Depends(db.get_db_session),
) -> Player:
    player = db.get_obj_of_type_by_id(player_id, Player, "Player", db_sess)
    player.score = 0.0
    return db.save_obj(player, db_sess)


def set_player_game_room(
    player_id: int,
    game: GameRoom,
    db_sess: Session = Depends(db.get_db_session),
) -> Player:
    player = db.get_obj_of_type_by_id(player_id, Player, "Player", db_sess)
    player.game_room = game
    player.game_room_id = game.id
    return db.save_obj(player, db_sess)


def reset_player_game_room(
    player_id: int,
    db_sess: Session = Depends(db.get_db_session),
) -> Player:
    player = db.get_obj_of_type_by_id(player_id, Player, "Player", db_sess)
    player.game_room = None
    player.game_room_id = None
    return db.save_obj(player, db_sess)
