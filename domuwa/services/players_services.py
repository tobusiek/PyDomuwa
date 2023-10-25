import fastapi
from sqlalchemy import exc, orm
from starlette import status

from domuwa import database as db
from domuwa import models, schemas


async def create_player(
    player: schemas.PlayerSchema,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Player:
    db_player = models.Player(name=player.name)
    try:
        db_player = await db.db_obj_save(db_player, db_sess)
    except exc.IntegrityError:
        raise fastapi.HTTPException(
            status.HTTP_400_BAD_REQUEST,
            "Player of given name already exists",
        )
    return db_player


async def get_all_players_from_game_room(
    game_room_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> list[models.Player]:
    return (
        db_sess.query(models.Player)
        .filter(models.Player.game_room_id == game_room_id)
        .all()
    )


async def update_player_name(
    player_id: int,
    new_name_player: schemas.PlayerSchema,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Player:
    player = await db.get_obj_of_type_by_id(player_id, models.Player, "Player", db_sess)
    player.name = new_name_player.name
    return await db.db_obj_save(player, db_sess)


async def update_player_score(
    player_id: int,
    points: float,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Player:
    player = await db.get_obj_of_type_by_id(player_id, models.Player, "Player", db_sess)
    player.score += points
    return await db.db_obj_save(player, db_sess)


async def reset_player_score(
    player_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Player:
    player = await db.get_obj_of_type_by_id(player_id, models.Player, "Player", db_sess)
    player.score = 0.0
    return await db.db_obj_save(player, db_sess)


async def set_player_game_room(
    player_id: int,
    game: models.GameRoom,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Player:
    player = await db.get_obj_of_type_by_id(player_id, models.Player, "Player", db_sess)
    player.game_room = game
    player.game_room_id = game.id
    return await db.db_obj_save(player, db_sess)


async def reset_player_game_room(
    player_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Player:
    player = await db.get_obj_of_type_by_id(player_id, models.Player, "Player", db_sess)
    player.game_room = None
    player.game_room_id = None
    return await db.db_obj_save(player, db_sess)
