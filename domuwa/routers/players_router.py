from typing import Type

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.responses import Response

from domuwa.database import db_obj_delete, get_all_objs_of_type, get_db, get_obj_of_type_by_id
from domuwa.models import Player
from domuwa.schemas import PlayerSchema, PlayerView
from domuwa.services import players_services as services

router = APIRouter(prefix="/player", tags=["Player"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_player(name: str, db: Session = Depends(get_db)):
    player = validate_player_data(name)
    db_player = await services.create_player(player, db)
    return create_player_view(db_player)


@router.get("/{player_id}")
async def get_player_by_id(player_id: int, db: Session = Depends(get_db)):
    player = await get_obj_of_type_by_id(player_id, Player, "Player", db)
    return create_player_view(player)


@router.get("/")
async def get_all_players(db: Session = Depends(get_db)):
    players = await get_all_objs_of_type(Player, db)
    return [create_player_view(player) for player in players]


@router.get("/from_game_room/{game_room_id}")
async def get_all_players_from_game_room(game_room_id: int, db: Session = Depends(get_db)):
    players = await services.get_all_players_from_game_room(game_room_id, db)
    return [create_player_view(player) for player in players]


@router.put("/update_name")
async def update_player_name(player_id: int, new_name: str, db: Session = Depends(get_db)):
    new_name_player = validate_player_data(new_name)
    player = await services.update_player_name(player_id, new_name_player, db)
    return create_player_view(player)


@router.put("/update_score")
async def update_player_score(player_id: int, points: float, db: Session = Depends(get_db)):
    player = await services.update_player_score(player_id, points, db)
    return create_player_view(player)


@router.put("/reset_game_room")
async def reset_player_game_room(player_id: int, db: Session = Depends(get_db)):
    player = await services.reset_player_game_room(player_id, db)
    return create_player_view(player)


@router.put("/reset_score")
async def reset_player_score(player_id: int, db: Session = Depends(get_db)):
    player = await services.reset_player_score(player_id, db)
    return create_player_view(player)


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_player(player_id: int, db: Session = Depends(get_db)):
    return await db_obj_delete(player_id, Player, "Player", db)


def validate_player_data(name: str) -> PlayerSchema:
    try:
        player = PlayerSchema(name=name)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid name provided")
    return player


def create_player_view(player: Player | Type[Player]) -> PlayerView:
    return PlayerView.model_validate(player)
