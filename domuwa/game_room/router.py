from typing import Type

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from domuwa.database import get_all_objs_of_type, get_db, get_obj_of_type_by_id
from domuwa.game_room import services
from domuwa.game_room.model import GameRoom
from domuwa.game_room.schema import GameRoomCreate, GameRoomView

router = APIRouter(prefix="/game_room", tags=["Game Room"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_game_room(name: str, category: str, db: Session = Depends(get_db)):
    game = GameRoomCreate(game_name=name, game_category=category)
    db_game_room = await services.create_game_room(game, db)
    return create_game_room_view(db_game_room)


@router.get("/{game_room_id}")
async def get_game_room_by_id(game_room_id: int, db: Session = Depends(get_db)):
    game = await get_obj_of_type_by_id(game_room_id, GameRoom, "GameRoom", db)
    return create_game_room_view(game)


@router.get("/")
async def get_all_game_rooms(db: Session = Depends(get_db)):
    game_rooms = await get_all_objs_of_type(GameRoom, db)
    return [create_game_room_view(game) for game in game_rooms]


@router.put("/add_player")
async def add_player(game_room_id: int, player_id: int, db: Session = Depends(get_db)):
    game = await services.add_player(game_room_id, player_id, db)
    return create_game_room_view(game)


@router.put("/remove_player")
async def remove_player(game_room_id: int, player_id: int, db: Session = Depends(get_db)):
    game = await services.remove_player(game_room_id, player_id, db)
    return create_game_room_view(game)


@router.put("/remove_player")
async def remove_players(game_room_id: int, db: Session = Depends(get_db)):
    game = await services.remove_all_players(game_room_id, db)
    return create_game_room_view(game)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_game_room(game_room_id: int, db: Session = Depends(get_db)):
    return await services.delete_game_room(game_room_id, db)


def create_game_room_view(game: GameRoom | Type[GameRoom]) -> GameRoomView:
    return GameRoomView.model_validate(game)
