from fastapi import APIRouter, Depends, HTTPException, Request, status
from pydantic import ValidationError
from sqlalchemy.orm import Session
from starlette.responses import Response

from domuwa import database as db
from domuwa import schemas
from domuwa.models import Question
from domuwa.services import questions_services as services
from domuwa.utils import logging

logger = logging.get_logger("domuwa")

router = APIRouter(prefix="/question", tags=["Question"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
def create_question(
    request: Request,
    game_name: str,
    category: str,
    author: str,
    text: str,
    db_sess: Session = Depends(db.get_db_session),
) -> schemas.QuestionSchema:
    question = validate_question_data(game_name, category, author, text)
    db_question = services.create_question(question, db_sess)
    return create_question_view(db_question)


@router.get("/{question_id}", response_model=None)
def get_question_by_id(
    request: Request,
    question_id: int,
    db_sess: Session = Depends(db.get_db_session),
) -> schemas.QuestionWithAnswersSchema:
    question = db.get_obj_of_type_by_id(
        question_id,
        Question,
        "Question",
        db_sess,
    )
    return create_question_view_with_answers(question)


@router.get("/", response_model=None)
def get_all_questions(
    request: Request,
    db_sess: Session = Depends(db.get_db_session),
) -> list[schemas.QuestionWithAnswersSchema]:
    questions = db.get_all_objs_of_type(Question, db_sess)
    return [create_question_view_with_answers(question) for question in questions]


@router.put("/", response_model=None)
def update_question(
    request: Request,
    question_id: int,
    game_name: str,
    category: str,
    author: str,
    text: str,
    excluded: bool,
    db_sess: Session = Depends(db.get_db_session),
) -> schemas.QuestionSchema:
    modified_question = validate_question_data(
        game_name,
        category,
        author,
        text,
        excluded,
    )
    db_question = services.update_question(
        question_id,
        modified_question,
        db_sess,
    )
    return create_question_view(db_question)


@router.put("/excluding", response_model=None)
def update_question_excluded(
    request: Request,
    question_id: int,
    excluded: bool,
    db_sess: Session = Depends(db.get_db_session),
) -> schemas.QuestionSchema:
    question = services.update_question_excluded(question_id, excluded, db_sess)
    return create_question_view(question)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
)
def delete_question(
    question_id: int,
    db_sess: Session = Depends(db.get_db_session),
) -> None:
    db.delete_obj(question_id, Question, "Question", db_sess)


def validate_question_data(
    game_name: str,
    category: str,
    author: str,
    text: str,
    excluded: bool = False,
) -> schemas.QuestionCreateSchema:
    try:
        question = schemas.QuestionCreateSchema(
            game_name=game_name,
            category=category,
            author=author,
            text=text,
            excluded=excluded,
        )
    except ValidationError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data input")
    return question


def create_question_view(question: Question) -> schemas.QuestionSchema:
    return schemas.QuestionSchema.model_validate(question)


def create_question_view_with_answers(
    question: Question,
) -> schemas.QuestionWithAnswersSchema:
    return schemas.QuestionWithAnswersSchema(
        id=question.id,
        game_name=question.game_name,
        category=question.category,
        author=question.author,
        text=question.text,
        excluded=question.excluded,
        answers=[
            schemas.AnswerSchema.model_validate(answer) for answer in question.answers
        ],
    )
