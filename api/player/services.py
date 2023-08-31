from typing import Type, Optional

from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from api.database import get_db
from api.player.model import Player
from api.player.schema import PlayerCreate

PLAYER_OF_ID_NOT_FOUND = "Player of id={} not found"
PLAYER_OF_NAME_NOT_FOUND = "Player of name={} not found"


async def create_player(player: PlayerCreate, db: Session = Depends(get_db)) -> Player:
    db_player = Player(name=player.name)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


async def get_player_by_id(player_id: int, db: Session = Depends(get_db)) -> Optional[Player]:
    player = db.query(Player).get(player_id)
    if not player:
        raise HTTPException(status.HTTP_404_NOT_FOUND, PLAYER_OF_ID_NOT_FOUND.format(player_id))
    return player


async def get_player_by_name(name: str, db: Session = Depends(get_db)) -> Optional[Type[Player]]:
    player = db.query(Player).filter(Player.name == name).first()
    if not player:
        raise HTTPException(status.HTTP_404_NOT_FOUND, PLAYER_OF_NAME_NOT_FOUND.format(name))
    return player


async def get_all_players(db: Session = Depends(get_db)) -> list[Type[Player]]:
    return db.query(Player).all()


async def get_all_players_from_game(game_id: int, db: Session = Depends(get_db)) -> list[Type[Player]]:
    return db.query(Player).filter(Player.game.id == game_id).all()


async def update_player_name_by_id(
        player_id: int,
        new_name_player: PlayerCreate,
        db: Session = Depends(get_db)
) -> Optional[Type[Player]]:
    player = db.query(Player).get(player_id)
    if not player:
        raise HTTPException(status.HTTP_404_NOT_FOUND, PLAYER_OF_ID_NOT_FOUND.format(player_id))
    player.name = new_name_player.name
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


async def update_player_name_by_name(
        old_name_player: PlayerCreate,
        new_name_player: PlayerCreate,
        db: Session = Depends(get_db)
) -> Optional[Type[Player]]:
    player = db.query(Player).filter(Player.name == old_name_player.name).first()
    if not player:
        raise HTTPException(status.HTTP_404_NOT_FOUND, PLAYER_OF_NAME_NOT_FOUND.format(old_name_player.name))
    player.name = new_name_player.name
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


async def update_player_score_by_id(
        player_id: int,
        points: float,
        db: Session = Depends(get_db)
) -> Optional[Type[Player]]:
    player = db.query(Player).get(player_id)
    if not player:
        raise HTTPException(status.HTTP_404_NOT_FOUND, PLAYER_OF_ID_NOT_FOUND.format(player_id))
    player.score += points
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


async def update_player_score_by_name(
        player: PlayerCreate,
        points: float,
        db: Session = Depends(get_db)
) -> Optional[Type[Player]]:
    player = db.query(Player).filter(Player.name == player.name).first()
    if not player:
        raise HTTPException(status.HTTP_404_NOT_FOUND, PLAYER_OF_NAME_NOT_FOUND.format(player.name))
    player.score += points
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


async def reset_player_score_by_id(player_id: int, db: Session = Depends(get_db)) -> Optional[Player]:
    player = db.query(Player).get(player_id)
    if not player:
        raise HTTPException(status.HTTP_404_NOT_FOUND, PLAYER_OF_ID_NOT_FOUND.format(player_id))
    player.score = 0
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


async def reset_player_score_by_name(player: PlayerCreate, db: Session = Depends(get_db)) -> Optional[Type[Player]]:
    player = db.query(Player).filter(Player.name == player.name).first()
    if not player:
        raise HTTPException(status.HTTP_404_NOT_FOUND, PLAYER_OF_NAME_NOT_FOUND.format(player.name))
    player.score = 0
    db.add(player)
    db.commit()
    db.refresh(player)
    return player


async def delete_player_by_id(player_id: int, db: Session = Depends(get_db)):
    db.query(Player).get(player_id).delete()
    db.commit()


async def delete_player_by_name(name: str, db: Session = Depends(get_db)):
    db.query(Player).filter(Player.name == name).delete()
    db.commit()
