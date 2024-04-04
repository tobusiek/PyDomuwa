from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlmodel import Session
from starlette.responses import JSONResponse

from domuwa.database import get_db_session
from domuwa.models.db_models import GameType
from domuwa.models.view_models import game_type as game_type_models
from domuwa.services import game_type_services as services

router = APIRouter(prefix="/game-types", tags=["Game Types"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create(
    new_game_type: game_type_models.GameTypeCreate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        game_type = GameType.model_validate(new_game_type, strict=True)
    except ValidationError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Provided invalid data"
        ) from exc

    db_game_type = await services.create_game_type(game_type, db_sess)
    return create_game_type_response(db_game_type, status.HTTP_201_CREATED)


@router.get("/{game_type_id}")
async def get_game_type_by_id(
    game_type_id: int, db_sess: Session = Depends(get_db_session)
):
    db_game_type = await services.get_game_type_by_id(game_type_id, db_sess)
    return create_game_type_response(db_game_type)


@router.get("/")
async def get_all_players(db_sess: Session = Depends(get_db_session)):
    db_game_types = await services.get_all_game_types(db_sess)
    read_game_types = []
    for db_game_type in db_game_types:
        try:
            read_game_types.append(
                game_type_models.GameTypeRead.model_validate(db_game_type)
            )
        except ValidationError as exc:
            raise HTTPException(
                status.HTTP_500_INTERNAL_SERVER_ERROR,
                "Cannot read Game Types from database",
            ) from exc
    return JSONResponse([game_type.model_dump() for game_type in read_game_types])


@router.patch("/{game_type_id}")
async def update_game_type(
    game_type_id: int,
    game_type_update: game_type_models.GameTypeUpdate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        game_type = GameType.model_validate(game_type_update, strict=True)
    except ValidationError as exc:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Provided invalid data"
        ) from exc

    db_game_type = await services.update_game_type(game_type_id, game_type, db_sess)
    return create_game_type_response(db_game_type)


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game_type(
    game_type_id: int, db_sess: Session = Depends(get_db_session)
):
    await services.delete_game_type(game_type_id, db_sess)


def create_game_type_response(
    db_game_type: GameType, status_code: int = status.HTTP_200_OK
):
    try:
        game_type_read = game_type_models.GameTypeRead.model_validate(db_game_type)
    except ValidationError as exc:
        raise HTTPException(
            status.HTTP_500_INTERNAL_SERVER_ERROR,
            "Cannot create GameType from database",
        ) from exc
    return JSONResponse(game_type_read.model_dump(), status_code)
