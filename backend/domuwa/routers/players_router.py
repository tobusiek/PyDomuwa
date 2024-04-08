import logging

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.requests import Request
from pydantic import ValidationError
from sqlmodel import Session

from domuwa.database import get_db_session
from domuwa.models.player import (
    Player,
    PlayerCreate,
    PlayerLogin,
    PlayerRead,
    PlayerSession,
    PlayerUpdate,
)
from domuwa.services import players_services as services

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", response_model=PlayerRead, status_code=status.HTTP_201_CREATED)
async def create_player(
    player_create: PlayerCreate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        logger.debug("received Player(%s) to create", player_create)
        player = Player.model_validate(player_create, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc

    return await services.create_player(player, db_sess)


@router.post("/login")
async def login(
    request: Request,
    player_login: PlayerLogin,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug("received Player(%s) to login", player_login)
    if request.session.get("player"):
        logger.warning(f"Player({player_login}) already logged in")
        return

    try:
        player = Player.model_validate(player_login, strict=True)
    except ValidationError as exc:
        err_msg = f"cannot parse PlayerLogin({player_login}) to Player"
        logger.error(err_msg)
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, err_msg) from exc

    db_player = await services.login_player(player, db_sess)
    try:
        player_session = PlayerSession.model_validate(db_player)
    except ValidationError as exc:
        err_msg = f"couldn't parse PlayerSession from Player({player})"
        logger.error(err_msg)
        raise HTTPException(status.HTTP_500_INTERNAL_SERVER_ERROR, err_msg) from exc

    request.session["player"] = player_session.model_dump()


@router.get("/{player_id}", response_model=PlayerRead)
async def get_player_by_id(player_id: int, db_sess: Session = Depends(get_db_session)):
    logger.debug("received Player(id=%d) to get", player_id)
    return await services.get_player_by_id(player_id, db_sess)


@router.get("/", response_model=list[PlayerRead])
async def get_all_players(db_sess: Session = Depends(get_db_session)):
    return await services.get_all_players(db_sess)


@router.patch("/{player_id}", response_model=PlayerRead)
async def update_player(
    player_id: int,
    player_update: PlayerUpdate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        logger.debug(
            "received Player(%s) to update Player(id=%d)",
            player_update,
            player_id,
        )
        player = Player.model_validate(player_update, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc

    return await services.update_player(player_id, player, db_sess)


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_player(player_id: int, db_sess: Session = Depends(get_db_session)):
    logger.debug(f"received Player(id={player_id}) to remove")
    await services.delete_player(player_id, db_sess)
