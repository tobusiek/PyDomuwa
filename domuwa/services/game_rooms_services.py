import fastapi
from sqlalchemy import orm

from domuwa import database as db
from domuwa import models, schemas
from domuwa.services import players_services


async def create_game_room(
    game: schemas.GameRoomSchema,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.GameRoom:
    db_game_room = models.GameRoom(
        game_name=game.game_name,
        game_category=game.game_category,
        players=[],
    )
    return await db.db_obj_save(db_game_room, db_sess)


async def add_player(
    game_room_id: int,
    player_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.GameRoom:
    player = await db.get_obj_of_type_by_id(player_id, models.Player, "Player", db_sess)
    game_room = await db.get_obj_of_type_by_id(game_room_id, models.GameRoom, "GameRoom", db_sess)
    player.game_room = game_room
    player.game_room_id = game_room_id
    if player not in game_room.players:
        await db.db_obj_save(player, db_sess)
        game_room.players.append(player)
    return await db.db_obj_save(game_room, db_sess)


async def remove_player(
    game_room_id: int,
    player_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.GameRoom:
    player = await db.get_obj_of_type_by_id(player_id, models.Player, "Player", db_sess)
    player.game_room = None
    player.game_room_id = None
    await db.db_obj_save(player, db_sess)
    game = await db.get_obj_of_type_by_id(game_room_id, models.GameRoom, "GameRoom", db_sess)
    game.players.remove(player)
    return await db.db_obj_save(game, db_sess)


async def remove_all_players(
    game_room_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.GameRoom:
    game = await db.get_obj_of_type_by_id(game_room_id, models.GameRoom, "GameRoom", db_sess)
    players = db_sess.query(models.Player).filter(models.Player.game_room_id == game_room_id).all()
    for player in players:
        await players_services.reset_player_game_room(player.id, db_sess)
    return await db.db_obj_save(game, db_sess)


async def delete_game_room(
    game_room_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> None:
    await db.db_obj_delete(game_room_id, models.GameRoom, "GameRoom", db_sess)
    players = db_sess.query(models.Player).filter(models.Player.game_room_id == game_room_id).all()
    for player in players:
        await players_services.reset_player_game_room(player.id, db_sess)
