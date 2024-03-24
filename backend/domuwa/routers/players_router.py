from fastapi import APIRouter, Depends, HTTPException, Request, status
from fastapi.responses import JSONResponse
from pydantic import ValidationError
from sqlmodel import Session
from starlette import responses

from domuwa.database import get_db_session
from domuwa.services import players_services as services
from domuwa.sqlmodels import player as player_models

router = APIRouter(prefix="/players", tags=["Players"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def create_player(
    request: Request,
    new_player: player_models.PlayerCreate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        player = player_models.Player.model_validate(new_player, strict=True)
    except ValidationError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Provided invalid data"
        ) from exc

    db_player = services.create_player(player, db_sess)
    db_player_data = db_player.model_dump()
    response = JSONResponse(db_player_data, status.HTTP_201_CREATED)

    if request.session.get("user") is None:
        response.set_cookie("user", db_player_data)
    return response


@router.get("/{player_id}")
def get_player_by_id(
    request: Request,
    player_id: int,
    db_sess: Session = Depends(get_db_session),
):
    player = services.get_player_by_id(player_id, db_sess)
    return JSONResponse(player.model_dump())


@router.get("/")
def get_all_players(
    request: Request,
    db_sess: Session = Depends(get_db_session),
):
    players = services.get_all_players(db_sess)
    return JSONResponse([player.model_dump() for player in players])


@router.patch("/{player_id}")
def update_player_name(
    request: Request,
    player_id: int,
    player_update: player_models.PlayerUpdate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        player = player_models.Player.model_validate(player_update, strict=True)
    except ValidationError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Provided invalid data"
        ) from exc

    return JSONResponse(
        services.update_player_name(player_id, player, db_sess).model_dump()
    )


@router.delete(
    "/{player_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=responses.Response,
    response_model=None,
)
def delete_player(
    player_id: int,
    db_sess: Session = Depends(get_db_session),
):
    services.delete_player(player_id, db_sess)
