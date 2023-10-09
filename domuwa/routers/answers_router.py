from domuwa.utils.logging import get_logger
from typing import Type

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.responses import Response

from domuwa import config
from domuwa.database import db_obj_delete, get_all_objs_of_type, get_db, get_obj_of_type_by_id
from domuwa.models import Answer
from domuwa.schemas import AnswerSchema, AnswerView, AnswerWithQuestionView, QuestionView
from domuwa.services import answers_services as services

logger = get_logger("domuwa")

router = APIRouter(prefix="/answer", tags=["Answer"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=AnswerWithQuestionView)
async def create_answer(
        author: str,
        text: str,
        question_id: int,
        correct: bool = False,
        db: Session = Depends(get_db),
) -> AnswerWithQuestionView:
    answer = validate_answer_data(author, text, correct, question_id)
    logger.debug(f"{answer=}")
    db_answer = await services.create_answer(answer, db)
    if config.TESTING:
        return create_answer_view_with_question(db_answer)


@router.get("/{answer_id}", response_model=AnswerWithQuestionView)
async def get_answer_by_id(answer_id: int, db: Session = Depends(get_db)) -> AnswerWithQuestionView:
    answer = await get_obj_of_type_by_id(answer_id, Answer, "Answer", db)
    if config.TESTING:
        return create_answer_view_with_question(answer)


@router.get("/")
async def get_all_answers(db: Session = Depends(get_db)) -> list[AnswerWithQuestionView]:
    answers = await get_all_objs_of_type(Answer, db)
    if config.TESTING:
        return [create_answer_view_with_question(answer) for answer in answers]


@router.get("/for_question/{question_id}")
async def get_answers_for_question(question_id: int, db: Session = Depends(get_db)) -> list[AnswerView]:
    answers = await services.get_answers_for_question(question_id, db)
    if config.TESTING:
        return [create_answer_view(answer) for answer in answers]


@router.put("/")
async def update_answer(
        answer_id: int,
        author: str,
        text: str,
        correct: bool,
        question_id: int,
        db: Session = Depends(get_db),
) -> AnswerWithQuestionView:
    modified_answer = validate_answer_data(author, text, correct, question_id)
    answer = await services.update_answer(answer_id, modified_answer, db)
    if config.TESTING:
        return create_answer_view_with_question(answer)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_answer(answer_id: int, db: Session = Depends(get_db)) -> None:
    if config.TESTING:
        return await db_obj_delete(answer_id, Answer, "Answer", db)


def validate_answer_data(author: str, text: str, correct: bool, question_id: int) -> AnswerSchema:
    try:
        answer = AnswerSchema(author=author, text=text, correct=correct, question_id=question_id)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data input")
    return answer


def create_answer_view(answer: Answer | Type[Answer]) -> AnswerView:
    return AnswerView.model_validate(answer)


def create_answer_view_with_question(answer: Answer | Type[Answer]) -> AnswerWithQuestionView:
    return AnswerWithQuestionView(
        id=answer.id,
        author=answer.author,
        text=answer.text,
        correct=answer.correct,
        question_id=answer.question_id,
        question=QuestionView.model_validate(answer.question),
    )
