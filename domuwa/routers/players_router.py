from typing import Type

from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette import templating
from starlette.responses import Response

from domuwa import config
from domuwa.database import (
    db_obj_delete,
    get_all_objs_of_type,
    get_db,
    get_obj_of_type_by_id,
)
from domuwa.models import Player
from domuwa.schemas import PlayerSchema, PlayerView
from domuwa.services import players_services as services

router = APIRouter(prefix="/player", tags=["Player"])
templates = templating.Jinja2Templates(directory="resources/templates")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_player(
    request: Request,
    name: str,
    db: Session = Depends(get_db),
) -> PlayerView | templating._TemplateResponse:
    player = validate_player_data(name)
    db_player = await services.create_player(player, db)
    player_view = create_player_view(db_player)
    if config.TESTING:
        return player_view
    ctx = {"request": request, "player": player_view.model_dump()}
    return templates.TemplateResponse("create_player.html", ctx)


@router.get("/{player_id}", response_model=None)
async def get_player_by_id(
    request: Request,
    player_id: int,
    db: Session = Depends(get_db),
) -> PlayerView | templating._TemplateResponse:
    player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    player_view = create_player_view(player)
    if config.TESTING:
        return player_view
    ctx = {"request": request, "player": player_view.model_dump()}
    return templates.TemplateResponse("get_player.html", ctx)


@router.get("/", response_model=None)
async def get_all_players(
    request: Request,
    db: Session = Depends(get_db),
) -> list[PlayerView] | templating._TemplateResponse:
    players = await get_all_objs_of_type(Player, db)
    player_views = [create_player_view(player) for player in players]
    if config.TESTING:
        return player_views
    ctx = {
        "request": request,
        "players": [player_view.model_dump() for player_view in player_views],
    }
    return templates.TemplateResponse("get_all_players.html", ctx)


@router.get("/from_game_room/{game_room_id}", response_model=None)
async def get_all_players_from_game_room(
    request: Request,
    game_room_id: int,
    db: Session = Depends(get_db),
) -> list[PlayerView] | templating._TemplateResponse:
    players = await services.get_all_players_from_game_room(game_room_id, db)
    player_views = [create_player_view(player) for player in players]
    if config.TESTING:
        return player_views
    ctx = {
        "request": request,
        "players": [player_view.model_dump() for player_view in player_views],
    }
    return templates.TemplateResponse("get_all_players_from_game.html", ctx)


@router.put("/update_name", response_model=None)
async def update_player_name(
    request: Request,
    player_id: int,
    new_name: str,
    db: Session = Depends(get_db),
) -> PlayerView | templating._TemplateResponse:
    new_name_player = validate_player_data(new_name)
    player = await services.update_player_name(player_id, new_name_player, db)
    player_view = create_player_view(player)
    if config.TESTING:
        return player_view
    ctx = {"request": request, "player": player_view.model_dump()}
    return templates.TemplateResponse("update_player.html", ctx)


@router.put("/update_score", response_model=None)
async def update_player_score(
    request: Request,
    player_id: int,
    points: float,
    db: Session = Depends(get_db),
) -> PlayerView | templating._TemplateResponse:
    player = await services.update_player_score(player_id, points, db)
    player_view = create_player_view(player)
    if config.TESTING:
        return player_view
    ctx = {"request": request, "player": player_view.model_dump()}
    return templates.TemplateResponse("update_player.html", ctx)


@router.put("/reset_game_room", response_model=None)
async def reset_player_game_room(
    request: Request,
    player_id: int,
    db: Session = Depends(get_db),
) -> PlayerView | templating._TemplateResponse:
    player = await services.reset_player_game_room(player_id, db)
    player_view = create_player_view(player)
    if config.TESTING:
        return player_view
    ctx = {"request": request, "player": player_view.model_dump()}
    return templates.TemplateResponse("update_player.html", ctx)


@router.put("/reset_score", response_model=None)
async def reset_player_score(
    request: Request,
    player_id: int,
    db: Session = Depends(get_db),
) -> PlayerView | templating._TemplateResponse:
    player = await services.reset_player_score(player_id, db)
    player_view = create_player_view(player)
    if config.TESTING:
        return player_view
    ctx = {"request": request, "player": player_view.model_dump()}
    return templates.TemplateResponse("update_player.html", ctx)


@router.delete(
    "/delete",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    response_model=None,
)
async def delete_player(player_id: int, db: Session = Depends(get_db)) -> None:
    await db_obj_delete(player_id, Player, "Player", db)


def validate_player_data(name: str) -> PlayerSchema:
    try:
        player = PlayerSchema(name=name)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid name provided")
    return player


def create_player_view(player: Player | Type[Player]) -> PlayerView:
    return PlayerView.model_validate(player)
