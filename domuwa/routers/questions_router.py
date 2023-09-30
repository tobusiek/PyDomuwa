from logging import getLogger
from typing import Type

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.responses import Response

from domuwa import config
from domuwa.database import db_obj_delete, get_all_objs_of_type, get_db, get_obj_of_type_by_id
from domuwa.models import Question
from domuwa.schemas import AnswerView, QuestionSchema, QuestionView, QuestionWithAnswersView
from domuwa.services import questions_services as services

logger = getLogger('domuwa')

router = APIRouter(prefix="/question", tags=["Question"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_question(game_name: str, category: str, author: str, text: str,
                          db: Session = Depends(get_db)) -> QuestionView:
    question = validate_question_data(game_name, category, author, text)
    if config.TESTING:
        return await services.create_question(question, db)


@router.get("/{question_id}")
async def get_question_by_id(question_id: int, db: Session = Depends(get_db)) -> QuestionWithAnswersView:
    question = await get_obj_of_type_by_id(question_id, Question, "Question", db)
    if config.TESTING:
        return create_question_view_with_answers(question)


@router.get("/")
async def get_all_questions(db: Session = Depends(get_db)) -> list[QuestionWithAnswersView]:
    questions = await get_all_objs_of_type(Question, db)
    if config.TESTING:
        return [create_question_view_with_answers(question) for question in questions]


@router.put("/")
async def update_question(
        question_id: int,
        game_name: str,
        category: str,
        author: str,
        text: str,
        db: Session = Depends(get_db),
) -> type[Question]:
    modified_question = validate_question_data(game_name, category, author, text)
    if config.TESTING:
        return await services.update_question(question_id, modified_question, db)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_question(question_id: int, db: Session = Depends(get_db)) -> None:
    if config.TESTING:
        return await db_obj_delete(question_id, Question, "Question", db)


def validate_question_data(game_name: str, category: str, author: str, text: str) -> QuestionSchema:
    try:
        question = QuestionSchema(game_name=game_name, category=category, author=author, text=text)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data input")
    return question


def create_question_view(question: Question | Type[Question]) -> QuestionView:
    return QuestionView.model_validate(question)


def create_question_view_with_answers(question: Question | Type[Question]) -> QuestionWithAnswersView:
    return QuestionWithAnswersView(
        id=question.id,
        game_name=question.game_name,
        category=question.category,
        author=question.author,
        text=question.text,
        excluded=question.excluded,
        answers=[AnswerView.model_validate(answer) for answer in question.answers],
    )
