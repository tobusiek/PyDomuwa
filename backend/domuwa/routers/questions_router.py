import logging

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlmodel import Session

from domuwa.database import get_db_session
from domuwa.models.question import (
    Question,
    QuestionCreate,
    QuestionRead,
    QuestionUpdate,
    QuestionWithAnswersRead,
)
from domuwa.services import questions_services as services

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questions", tags=["Question"])


@router.post("/", response_model=QuestionRead, status_code=status.HTTP_201_CREATED)
async def create_question(
    question_create: QuestionCreate, db_sess: Session = Depends(get_db_session)
):
    logger.debug("received Question(%s) to create", question_create)
    try:
        question = Question.model_validate(question_create, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_422_UNPROCESSABLE_ENTITY, str(exc)) from exc

    return await services.create_question(question, db_sess)


@router.get("/{question_id}", response_model=QuestionWithAnswersRead)
async def get_question_by_id(
    question_id: int,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug("received Question(id=%d) to get", question_id)
    return await services.get_question_by_id(question_id, db_sess)


@router.get("/", response_model=list[QuestionWithAnswersRead])
async def get_all_questions(db_sess: Session = Depends(get_db_session)):
    return await services.get_all_questions(db_sess)


@router.patch("/{question_id}", response_model=QuestionWithAnswersRead)
async def update_question(
    question_id: int,
    question_update: QuestionUpdate,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug(
        "received Question(%s) to update Question(id=%d)", question_update, question_id
    )
    question = await services.get_question_by_id(question_id, db_sess)
    return await services.update_question(question_update, question, db_sess)


@router.delete("/{question_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_question(question_id: int, db_sess: Session = Depends(get_db_session)):
    logger.debug("received Question(id=%d) to remove", question_id)
    await services.delete_question(question_id, db_sess)
