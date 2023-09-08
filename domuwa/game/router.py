from typing import Type

from fastapi import APIRouter, Depends, HTTPException, Response, status
from pydantic import ValidationError
from sqlalchemy.orm import Session

from domuwa.database import get_all_objs_of_type, get_db, get_obj_of_type_by_id
from domuwa.game import services
from domuwa.game.model import Game
from domuwa.game.schema import GameCreate, GameView

router = APIRouter(prefix="/game", tags=["Game"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_game(name: str, category: str, db: Session = Depends(get_db)):
    try:
        game = GameCreate(name=name, category=category)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data input")
    db_game = await services.create_game(game, db)
    return create_game_view(db_game)


@router.get("/{game_id}")
async def get_game_by_id(game_id: int, db: Session = Depends(get_db)):
    game = await get_obj_of_type_by_id(game_id, Game, "Game", db)
    return create_game_view(game)


@router.get("/")
async def get_all_games(db: Session = Depends(get_db)):
    games = await get_all_objs_of_type(Game, db)
    return [create_game_view(game) for game in games]


@router.put("/add_player")
async def add_player(game_id: int, player_id: int, db: Session = Depends(get_db)):
    game = await services.add_player(game_id, player_id, db)
    return create_game_view(game)


@router.put("/remove_player")
async def remove_player(game_id: int, player_id: int, db: Session = Depends(get_db)):
    game = await services.remove_player(game_id, player_id, db)
    return create_game_view(game)


@router.put("/remove_player")
async def remove_players(game_id: int, db: Session = Depends(get_db)):
    game = await services.remove_all_players(game_id, db)
    return create_game_view(game)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_game(game_id: int, db: Session = Depends(get_db)):
    return await services.delete_game(game_id, db)


def create_game_view(game: Game | Type[Game]) -> GameView:
    return GameView.model_validate(game)
