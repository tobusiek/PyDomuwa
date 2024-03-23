from fastapi import APIRouter, Depends, Request, status
from sqlalchemy.orm import Session
from starlette.responses import Response

from domuwa import database as db
from domuwa import schemas
from domuwa.models import GameRoom
from domuwa.services import game_rooms_services as services

router = APIRouter(prefix="/game_room", tags=["Game Room"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def create_game_room(
    request: Request,
    name: str,
    category: str,
    db_sess: Session = Depends(db.get_db_session),
) -> schemas.GameRoomSchema:
    game = schemas.GameRoomCreateSchema(game_name=name, game_category=category)
    db_game_room = services.create_game_room(game, db_sess)
    return create_game_room_view(db_game_room)


@router.get("/{game_room_id}", response_model=None)
def get_game_room_by_id(
    request: Request,
    game_room_id: int,
    db_sess: Session = Depends(db.get_db_session),
) -> schemas.GameRoomSchema:
    game_room = db.get_obj_of_type_by_id(
        game_room_id,
        GameRoom,
        "GameRoom",
        db_sess,
    )
    return create_game_room_view(game_room)


@router.get("/", response_model=None)
def get_all_game_rooms(
    request: Request,
    db_sess: Session = Depends(db.get_db_session),
) -> list[schemas.GameRoomSchema]:
    game_rooms = db.get_all_objs_of_type(GameRoom, db_sess)
    return [create_game_room_view(game) for game in game_rooms]


@router.put("/add_player", response_model=None)
def add_player(
    request: Request,
    game_room_id: int,
    player_id: int,
    db_sess: Session = Depends(db.get_db_session),
) -> schemas.GameRoomSchema:
    game_room = services.add_player(game_room_id, player_id, db_sess)
    return create_game_room_view(game_room)


@router.put("/remove_player", response_model=None)
def remove_player(
    request: Request,
    game_room_id: int,
    player_id: int,
    db_sess: Session = Depends(db.get_db_session),
) -> schemas.GameRoomSchema:
    game_room = services.remove_player(game_room_id, player_id, db_sess)
    return create_game_room_view(game_room)


@router.put("/remove_player", response_model=None)
def remove_players(
    request: Request,
    game_room_id: int,
    db_sess: Session = Depends(db.get_db_session),
) -> schemas.GameRoomSchema:
    game_room = services.remove_all_players(game_room_id, db_sess)
    return create_game_room_view(game_room)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    response_model=None,
)
def delete_game_room(
    game_room_id: int,
    db_sess: Session = Depends(db.get_db_session),
) -> None:
    services.delete_game_room(game_room_id, db_sess)


def create_game_room_view(game: GameRoom) -> schemas.GameRoomSchema:
    return schemas.GameRoomSchema.model_validate(game)
