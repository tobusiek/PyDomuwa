from typing import Optional, Type

from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.responses import Response

from api.database import get_db
from api.player import services
from api.player.schema import PlayerCreate, PlayerView
from db.schemas import Player

router = APIRouter(prefix="/player", tags=["Player"])

INVALID_DATA_INPUT = "Invalid data input"


@router.post("/", status_code=status.HTTP_200_OK, response_model=PlayerView)
async def create_player(name: str, db: Session = Depends(get_db)) -> PlayerView:
    try:
        player = PlayerCreate(name=name)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, INVALID_DATA_INPUT + ": name")
    db_player = await services.create_player(player, db)
    return db_player
    # player_view = PlayerView(
    #     id=db_player.id,
    #     games_played=db_player.games_played,
    #     games_won=db_player.games_won,
    #     score=db_player.score,
    #     game=db_player.game
    # )
    # return player_view


@router.get("/{player_id}", status_code=status.HTTP_200_OK, response_model=PlayerView)
async def get_player_by_id(player_id: int, db: Session = Depends(get_db)) -> Optional[Player]:
    return await services.get_player_by_id(player_id, db)


@router.get("/{player_name}", status_code=status.HTTP_200_OK, response_model=PlayerView)
async def get_player_by_name(name: str, db: Session = Depends(get_db)) -> Optional[Player]:
    return await services.get_player_by_name(name, db)


@router.get("/", status_code=status.HTTP_200_OK, response_model=list[PlayerView])
async def get_all_players(db: Session = Depends(get_db)) -> list[Type[Player]]:
    return await services.get_all_players(db)
    # return [PlayerView(
    #     id=player.id,
    #     games_played=player.games_played,
    #     games_won=player.games_won,
    #     score=player.score,
    #     game=player.game
    # ) for player in await services.get_all_players(db)]


@router.get("/{game_id}", status_code=status.HTTP_200_OK, response_model=list[PlayerView])
async def get_all_players_from_game(game_id: int, db: Session = Depends(get_db)) -> list[Type[Player]]:
    return await services.get_all_players_from_game(game_id, db)


@router.put("/", status_code=status.HTTP_200_OK, response_model=PlayerView)
async def update_player_name_by_id(player_id: int, new_name: str, db: Session = Depends(get_db)) -> Optional[Player]:
    try:
        new_name_player = PlayerCreate(name=new_name)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, INVALID_DATA_INPUT + ": new name")
    return await services.update_player_name_by_id(player_id, new_name_player, db)


@router.put("/", status_code=status.HTTP_200_OK, response_model=PlayerView)
async def update_player_name_by_name(old_name: str, new_name: str, db: Session = Depends(get_db)) -> Optional[Player]:
    try:
        old_name_player = PlayerCreate(name=old_name)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, INVALID_DATA_INPUT + ": old name")
    try:
        new_name_player = PlayerCreate(name=new_name)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, INVALID_DATA_INPUT + ": new name")
    return await services.update_player_name_by_name(old_name_player, new_name_player, db)


@router.put("/", status_code=status.HTTP_200_OK, response_model=PlayerView)
async def update_player_score_by_id(player_id: int, points: float, db: Session = Depends(get_db)) -> Optional[Player]:
    return await services.update_player_score_by_id(player_id, points, db)


@router.put("/", status_code=status.HTTP_200_OK, response_model=PlayerView)
async def update_player_score_by_name(name: str, points: float, db: Session = Depends(get_db)) -> Optional[Player]:
    try:
        player = PlayerCreate(name=name)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, INVALID_DATA_INPUT + ": name")
    return await services.update_player_score_by_name(player, points, db)


@router.put("/", status_code=status.HTTP_200_OK, response_model=PlayerView)
async def reset_player_score_by_id(player_id: int, db: Session = Depends(get_db)) -> Optional[Player]:
    return await services.reset_player_score_by_id(player_id, db)


@router.put("/", status_code=status.HTTP_200_OK, response_model=PlayerView)
async def reset_player_score_by_name(name: str, db: Session = Depends(get_db)) -> Optional[Player]:
    try:
        player = PlayerCreate(name=name)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, INVALID_DATA_INPUT + ": name")
    return await services.reset_player_score_by_name(player, db)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_player_by_id(player_id: int, db: Session = Depends(get_db)) -> None:
    return await services.delete_player_by_id(player_id, db)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_player_by_name(name: str, db: Session = Depends(get_db)) -> None:
    return await services.delete_player_by_name(name, db)
