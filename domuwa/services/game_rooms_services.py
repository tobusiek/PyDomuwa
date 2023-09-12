from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

import domuwa.services.players_services as player_services
from domuwa.database import db_obj_delete, db_obj_save, get_db, get_obj_of_type_by_id
from domuwa.models import GameRoom, Player
from domuwa.schemas import GameRoomSchema


async def create_game_room(game: GameRoomSchema, db: Session = Depends(get_db)) -> GameRoom:
    db_game_room = GameRoom(
        game_name=game.game_name,
        game_category=game.game_category,
        players=[],
    )
    return await db_obj_save(db_game_room, db)


async def add_player(game_room_id: int, player_id: int, db: Session = Depends(get_db)) -> Type[GameRoom]:
    player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    game_room = await get_obj_of_type_by_id(game_room_id, GameRoom, "GameRoom", db)
    player.game_room = game_room
    player.game_room_id = game_room_id
    if player not in game_room.players:
        await db_obj_save(player, db)
        game_room.players.append(player)
    return await db_obj_save(game_room, db)


async def remove_player(game_room_id: int, player_id: int, db: Session = Depends(get_db)) -> Type[GameRoom]:
    player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    player.game_room = None
    player.game_room_id = None
    await db_obj_save(player, db)
    game = await get_obj_of_type_by_id(game_room_id, GameRoom, "GameRoom", db)
    game.players.remove(player)
    return await db_obj_save(game, db)


async def remove_all_players(game_room_id: int, db: Session = Depends(get_db)) -> Type[GameRoom]:
    game = await get_obj_of_type_by_id(game_room_id, GameRoom, "GameRoom", db)
    players = db.query(Player).filter(Player.game_room_id == game_room_id).all()
    for players in players:
        await player_services.reset_player_game_room(players.id, db)
    return await db_obj_save(game, db)


async def delete_game_room(game_room_id: int, db: Session = Depends(get_db)) -> None:
    await db_obj_delete(game_room_id, GameRoom, "GameRoom", db)
    players = db.query(Player).filter(Player.game_room_id == game_room_id).all()
    for player in players:
        await player_services.reset_player_game_room(player.id, db)
    return None
