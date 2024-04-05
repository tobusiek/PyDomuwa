import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlmodel import Session

from domuwa.database import get_db_session
from domuwa.models.db_models import GameType
from domuwa.models.view_models import game_type as game_type_models
from domuwa.services import game_type_services as services

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/game-types", tags=["Game Types"])


@router.post(
    "/",
    response_model=game_type_models.GameTypeRead,
    status_code=status.HTTP_201_CREATED,
)
async def create(
    new_game_type: game_type_models.GameTypeCreate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        logger.debug(f"received GameType({new_game_type}) to create")
        game_type = GameType.model_validate(new_game_type, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Provided invalid data"
        ) from exc

    return await services.create_game_type(game_type, db_sess)


@router.get("/{game_type_id}", response_model=game_type_models.GameTypeRead)
async def get_game_type_by_id(
    game_type_id: int, db_sess: Session = Depends(get_db_session)
):
    return await services.get_game_type_by_id(game_type_id, db_sess)


@router.get("/", response_model=list[game_type_models.GameTypeRead])
async def get_all_players(db_sess: Session = Depends(get_db_session)):
    return await services.get_all_game_types(db_sess)


@router.patch("/{game_type_id}", response_model=game_type_models.GameTypeRead)
async def update_game_type(
    game_type_id: int,
    game_type_update: game_type_models.GameTypeUpdate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        logger.debug(
            f"received GameType({game_type_update}) to update GameType(id={game_type_id})"
        )
        game_type = GameType.model_validate(game_type_update, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "Provided invalid data"
        ) from exc

    return await services.update_game_type(game_type_id, game_type, db_sess)


@router.delete("/{game_type_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_game_type(
    game_type_id: int, db_sess: Session = Depends(get_db_session)
):
    logger.debug(f"received GameType(id={game_type_id}) to remove")
    await services.delete_game_type(game_type_id, db_sess)
