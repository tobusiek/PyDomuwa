from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlmodel import Session

from domuwa.database import get_db_session
from domuwa.models.db_models import Player
from domuwa.models.view_models import player as player_models
from domuwa.services import players_services as services

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_player(
    new_player: player_models.PlayerCreate, db_sess: Session = Depends(get_db_session)
):
    try:
        player = Player.model_validate(new_player, strict=True)
    except ValidationError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Provided invalid data"
        ) from exc

    db_player = await services.create_player(player, db_sess)
    return create_player_response(db_player, status.HTTP_201_CREATED)


@router.get("/{player_id}")
async def get_player_by_id(player_id: int, db_sess: Session = Depends(get_db_session)):
    db_player = await services.get_player_by_id(player_id, db_sess)
    return create_player_response(db_player)


@router.get("/")
async def get_all_players(db_sess: Session = Depends(get_db_session)):
    db_players = await services.get_all_players(db_sess)
    read_players = []
    for db_player in db_players:
        try:
            read_players.append(player_models.PlayerRead.model_validate(db_player))
        except ValidationError as exc:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Cannot create Players from database",
            ) from exc
    return JSONResponse([player.model_dump() for player in read_players])


@router.patch("/{player_id}")
async def update_player(
    player_id: int,
    player_update: player_models.PlayerUpdate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        player = Player.model_validate(player_update, strict=True)
    except ValidationError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Provided invalid data"
        ) from exc

    db_player = await services.update_player(player_id, player, db_sess)
    return create_player_response(db_player)


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_id: int, db_sess: Session = Depends(get_db_session)):
    await services.delete_player(player_id, db_sess)


def create_player_response(db_player: Player, status_code: int = status.HTTP_200_OK):
    try:
        player_read = player_models.PlayerRead.model_validate(db_player)
    except ValidationError as exc:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Cannot create Player from database",
        ) from exc
    return JSONResponse(player_read.model_dump(), status_code)
