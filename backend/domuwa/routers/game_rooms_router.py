import fastapi
from fastapi import status
from sqlalchemy import orm
from starlette import templating

from domuwa import config, models, schemas
from domuwa import database as db
from domuwa.services import game_rooms_services as services

router = fastapi.APIRouter(prefix="/game_room", tags=["Game Room"])
templates = templating.Jinja2Templates(directory="resources/templates")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_game_room(
    request: fastapi.Request,
    name: str,
    category: str,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.GameRoomView | templating._TemplateResponse:
    game = schemas.GameRoomSchema(game_name=name, game_category=category)
    db_game_room = await services.create_game_room(game, db_sess)
    game_room_view = create_game_room_view(db_game_room)
    if config.TESTING:
        return game_room_view
    ctx = {"request": request, "game_room": game_room_view.model_dump()}
    return templates.TemplateResponse("create_game_room.html", ctx)


@router.get("/{game_room_id}", response_model=None)
async def get_game_room_by_id(
    request: fastapi.Request,
    game_room_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.GameRoomView | templating._TemplateResponse:
    game_room = await db.get_obj_of_type_by_id(
        game_room_id,
        models.GameRoom,
        "GameRoom",
        db_sess,
    )
    game_room_view = create_game_room_view(game_room)
    if config.TESTING:
        return game_room_view
    ctx = {"request": request, "game_room": game_room_view.model_dump()}
    return templates.TemplateResponse("get_game_room.html", ctx)


@router.get("/", response_model=None)
async def get_all_game_rooms(
    request: fastapi.Request,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> list[schemas.GameRoomView] | templating._TemplateResponse:
    game_rooms = await db.get_all_objs_of_type(models.GameRoom, db_sess)
    game_room_views = [create_game_room_view(game) for game in game_rooms]
    if config.TESTING:
        return game_room_views
    ctx = {
        "request": request,
        "game_rooms": [
            game_room_view.model_dump() for game_room_view in game_room_views
        ],
    }
    return templates.TemplateResponse("get_all_game_rooms.html", ctx)


@router.put("/add_player", response_model=None)
async def add_player(
    request: fastapi.Request,
    game_room_id: int,
    player_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.GameRoomView | templating._TemplateResponse:
    game_room = await services.add_player(game_room_id, player_id, db_sess)
    game_room_views = create_game_room_view(game_room)
    if config.TESTING:
        return game_room_views
    ctx = {"request": request, "game_room": game_room_views.model_dump()}
    return templates.TemplateResponse("game_room_add_player.html", ctx)


@router.put("/remove_player", response_model=None)
async def remove_player(
    request: fastapi.Request,
    game_room_id: int,
    player_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.GameRoomView | templating._TemplateResponse:
    game_room = await services.remove_player(game_room_id, player_id, db_sess)
    game_room_view = create_game_room_view(game_room)
    if config.TESTING:
        return game_room_view
    ctx = {"request": request, "game_room_view": game_room_view.model_dump()}
    return templates.TemplateResponse("game_room_add_player.html", ctx)


@router.put("/remove_player", response_model=None)
async def remove_players(
    request: fastapi.Request,
    game_room_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.GameRoomView | templating._TemplateResponse:
    game_room = await services.remove_all_players(game_room_id, db_sess)
    game_room_view = create_game_room_view(game_room)
    if config.TESTING:
        return game_room_view
    ctx = {"request": request, "game_room": game_room_view.model_dump()}
    return templates.TemplateResponse("game_room_remove_player.html", ctx)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=fastapi.Response,
    response_model=None,
)
async def delete_game_room(
    game_room_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> None:
    await services.delete_game_room(game_room_id, db_sess)


def create_game_room_view(game: models.GameRoom) -> schemas.GameRoomView:
    return schemas.GameRoomView.model_validate(game)
