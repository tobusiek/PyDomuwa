import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlmodel import Session

from domuwa.database import get_db_session
from domuwa.models.answer import (
    Answer,
    AnswerCreate,
    AnswerUpdate,
    AnswerWithQuestionRead,
)
from domuwa.services import answers_services as services

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/answers", tags=["Answer"])


@router.post(
    "/", response_model=AnswerWithQuestionRead, status_code=status.HTTP_201_CREATED
)
async def create_answer(
    answer_create: AnswerCreate,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug("received Answer(%s) to create", answer_create)
    try:
        answer = Answer.model_validate(answer_create, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc

    return await services.create_answer(answer, db_sess)


@router.get("/{answer_id}", response_model=AnswerWithQuestionRead)
async def get_answer_by_id(answer_id: int, db_sess: Session = Depends(get_db_session)):
    logger.debug("received Answer(id=%d) to get", answer_id)
    return await services.get_answer_by_id(answer_id, db_sess)


@router.get("/", response_model=list[AnswerWithQuestionRead])
async def get_all_answers(db_sess: Session = Depends(get_db_session)):
    return await services.get_all_answers(db_sess)


@router.patch("/{answer_id}", response_model=AnswerWithQuestionRead)
async def update_answer(
    answer_id: int,
    answer_update: AnswerUpdate,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug(
        "received Answer(%s) to update Answer(id=%d)", answer_update, answer_id
    )
    try:
        answer = Answer.model_validate(answer_update, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc

    return await services.update_answer(answer_id, answer, db_sess)


@router.delete("/{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_answer(answer_id: int, db_sess: Session = Depends(get_db_session)):
    logger.debug("received Answer(id=%d) to remove", answer_id)
    await services.delete_answer(answer_id, db_sess)
