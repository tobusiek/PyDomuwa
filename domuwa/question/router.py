from typing import Type

from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.responses import Response

from domuwa.database import db_obj_delete, get_all_objs_of_type, get_db, get_obj_of_type_by_id
from domuwa.question import services
from domuwa.question.model import Question
from domuwa.question.schema import QuestionCreate, QuestionView

router = APIRouter(prefix="/question", tags=["Question"])


@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_question(game_name: str, category: str, author: str, text: str, db: Session = Depends(get_db)):
    question = validate_question_data(game_name, category, author, text)
    return await services.create_question(question, db)


@router.get("/")
async def get_question_by_id(question_id: int, db: Session = Depends(get_db)):
    return await get_obj_of_type_by_id(question_id, Question, "Question", db)


@router.get("/", response_model=list[Type[Question]])
async def get_all_questions(db: Session = Depends(get_db)):
    return await get_all_objs_of_type(Question, db)


@router.put("/")
async def update_question(
        question_id: int,
        game_name: str,
        category: str,
        author: str,
        text: str,
        db: Session = Depends(get_db)
):
    modified_question = validate_question_data(game_name, category, author, text)
    return await services.update_question(question_id, modified_question, db)


@router.delete("/", status_code=status.HTTP_204_NO_CONTENT, response_class=Response)
async def delete_question(question_id: int, db: Session = Depends(get_db)):
    return await db_obj_delete(question_id, Question, "Question", db)


def validate_question_data(game_name: str, category: str, author: str, text: str) -> QuestionCreate:
    try:
        question = QuestionCreate(game_name=game_name, category=category, author=author, text=text)
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data input")
    return question


def create_question_view(question: Question | Type[Question]) -> QuestionView:
    return QuestionView.model_validate(question)
