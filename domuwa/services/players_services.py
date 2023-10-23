from typing import Type

from fastapi import Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from starlette import status

from domuwa.database import db_obj_save, get_db, get_obj_of_type_by_id
from domuwa.models import GameRoom, Player
from domuwa.schemas import PlayerSchema


async def create_player(player: PlayerSchema, db: Session = Depends(get_db)) -> Player:
    db_player = Player(name=player.name)  # type: ignore
    try:
        db_player = await db_obj_save(db_player, db)
    except IntegrityError:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Player of given name already exists",
        )
    return db_player


async def get_all_players_from_game_room(
    game_room_id: int,
    db: Session = Depends(get_db),
) -> list[Player]:
    return db.query(Player).filter(Player.game_room_id == game_room_id).all()


async def update_player_name(
    player_id: int,
    new_name_player: PlayerSchema,
    db: Session = Depends(get_db),
) -> Type[Player]:
    player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    player.name = new_name_player.name
    return await db_obj_save(player, db)


async def update_player_score(
    player_id: int,
    points: float,
    db: Session = Depends(get_db),
) -> Type[Player]:
    player: Player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    player.score += points
    return await db_obj_save(player, db)


async def reset_player_score(
    player_id: int,
    db: Session = Depends(get_db),
) -> Type[Player]:
    player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    player.score = 0.0
    return await db_obj_save(player, db)


async def set_player_game_room(
    player_id: int,
    game: GameRoom,
    db: Session = Depends(get_db),
) -> Type[Player]:
    player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    player.game_room = game
    player.game_room_id = game.id
    return await db_obj_save(player, db)


async def reset_player_game_room(
    player_id: int,
    db: Session = Depends(get_db),
) -> Type[Player]:
    player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    player.game_room = None
    player.game_room_id = None
    return await db_obj_save(player, db)
