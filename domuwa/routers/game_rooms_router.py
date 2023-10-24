from typing import Type

from fastapi import APIRouter, Depends, Request, Response, status
from sqlalchemy.orm import Session
from starlette import templating

from domuwa import config
from domuwa.database import get_all_objs_of_type, get_db, get_obj_of_type_by_id
from domuwa.models import GameRoom
from domuwa.schemas import GameRoomSchema, GameRoomView
from domuwa.services import game_rooms_services as services

router = APIRouter(prefix="/game_room", tags=["Game Room"])
templates = templating.Jinja2Templates(directory="resources/templates")


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_game_room(
    request: Request,
    name: str,
    category: str,
    db: Session = Depends(get_db),
) -> GameRoomView | templating._TemplateResponse:
    game = GameRoomSchema(game_name=name, game_category=category)
    db_game_room = await services.create_game_room(game, db)
    game_room_view = create_game_room_view(db_game_room)
    if config.TESTING:
        return game_room_view
    ctx = {"request": request, "game_room": game_room_view.model_dump()}
    return templates.TemplateResponse("create_game_room.html", ctx)


@router.get("/{game_room_id}")
async def get_game_room_by_id(
    request: Request,
    game_room_id: int,
    db: Session = Depends(get_db),
) -> GameRoomView | templating._TemplateResponse:
    game_room = await get_obj_of_type_by_id(game_room_id, GameRoom, "GameRoom", db)
    game_room_view = create_game_room_view(game_room)
    if config.TESTING:
        return game_room_view
    ctx = {"request": request, "game_room": game_room_view.model_dump()}
    return templates.TemplateResponse("get_game_room.html", ctx)


@router.get("/")
async def get_all_game_rooms(
    request: Request,
    db: Session = Depends(get_db),
) -> list[GameRoomView] | templating._TemplateResponse:
    game_rooms = await get_all_objs_of_type(GameRoom, db)
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


@router.put("/add_player")
async def add_player(
    request: Request,
    game_room_id: int,
    player_id: int,
    db: Session = Depends(get_db),
) -> GameRoomView | templating._TemplateResponse:
    game_room = await services.add_player(game_room_id, player_id, db)
    game_room_views = create_game_room_view(game_room)
    if config.TESTING:
        return game_room_views
    ctx = {"request": request, "game_room": game_room_views.model_dump()}
    return templates.TemplateResponse("game_room_add_player.html", ctx)


@router.put("/remove_player")
async def remove_player(
    request: Request,
    game_room_id: int,
    player_id: int,
    db: Session = Depends(get_db),
) -> GameRoomView | templating._TemplateResponse:
    game_room = await services.remove_player(game_room_id, player_id, db)
    game_room_view = create_game_room_view(game_room)
    if config.TESTING:
        return game_room_view
    ctx = {"request": request, "game_room_view": game_room_view.model_dump()}
    return templates.TemplateResponse("game_room_add_player.html", ctx)


@router.put("/remove_player")
async def remove_players(
    request: Request,
    game_room_id: int,
    db: Session = Depends(get_db),
) -> GameRoomView | templating._TemplateResponse:
    game_room = await services.remove_all_players(game_room_id, db)
    game_room_view = create_game_room_view(game_room)
    if config.TESTING:
        return game_room_view
    ctx = {"request": request, "game_room": game_room_view.model_dump()}
    return templates.TemplateResponse("game_room_remove_player.html", ctx)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_game_room(game_room_id: int, db: Session = Depends(get_db)) -> None:
    await services.delete_game_room(game_room_id, db)


def create_game_room_view(game: GameRoom | Type[GameRoom]) -> GameRoomView:
    return GameRoomView.model_validate(game)
