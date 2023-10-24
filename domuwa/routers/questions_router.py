from typing import Type

from fastapi import APIRouter, Depends, HTTPException, Request, status
from sqlalchemy.orm import Session
from starlette import templating
from starlette.responses import Response

from domuwa import config
from domuwa.database import (
    db_obj_delete,
    get_all_objs_of_type,
    get_db,
    get_obj_of_type_by_id,
)
from domuwa.models import Question
from domuwa.schemas import (
    AnswerView,
    QuestionSchema,
    QuestionView,
    QuestionWithAnswersView,
)
from domuwa.services import questions_services as services
from domuwa.utils.logging import get_logger

logger = get_logger("domuwa")

router = APIRouter(prefix="/question", tags=["Question"])
templates = templating.Jinja2Templates(directory="resources/templates")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_question(
    request: Request,
    game_name: str,
    category: str,
    author: str,
    text: str,
    db: Session = Depends(get_db),
) -> QuestionView | templating._TemplateResponse:
    question = validate_question_data(game_name, category, author, text)
    db_question = await services.create_question(question, db)
    question_view = create_question_view(db_question)
    if config.TESTING:
        return question_view
    ctx = {"request": request, "question": question_view.model_dump()}
    return templates.TemplateResponse("create_question.html", ctx)


@router.get("/{question_id}", response_model=None)
async def get_question_by_id(
    request: Request,
    question_id: int,
    db: Session = Depends(get_db),
) -> QuestionWithAnswersView | templating._TemplateResponse:
    question = await get_obj_of_type_by_id(question_id, Question, "Question", db)
    question_view = create_question_view_with_answers(question)
    if config.TESTING:
        return question_view
    ctx = {"request": request, "question": question_view.model_dump()}
    return templates.TemplateResponse("get_question.html", ctx)


@router.get("/", response_model=None)
async def get_all_questions(
    request: Request,
    db: Session = Depends(get_db),
) -> list[QuestionWithAnswersView] | templating._TemplateResponse:
    questions = await get_all_objs_of_type(Question, db)
    question_views = [
        create_question_view_with_answers(question) for question in questions
    ]
    if config.TESTING:
        return question_views
    ctx = {
        "request": request,
        "questions": [question_view.model_dump() for question_view in question_views],
    }
    return templates.TemplateResponse("get_all_questions.html", ctx)


@router.put("/", response_model=None)
async def update_question(
    request: Request,
    question_id: int,
    game_name: str,
    category: str,
    author: str,
    text: str,
    db: Session = Depends(get_db),
) -> QuestionView | templating._TemplateResponse:
    modified_question = validate_question_data(game_name, category, author, text)
    db_question = await services.update_question(question_id, modified_question, db)
    question_view = create_question_view(db_question)
    if config.TESTING:
        return question_view
    ctx = {"request": request, "question": question_view.model_dump()}
    return templates.TemplateResponse("update_question.html", ctx)


@router.put("/excluding", response_model=None)
async def update_question_excluded(
    request: Request,
    question_id: int,
    excluded: bool,
    db: Session = Depends(get_db),
) -> QuestionView | templating._TemplateResponse:
    question = await services.update_question_excluded(question_id, excluded, db)
    question_view = create_question_view(question)
    if config.TESTING:
        return question_view
    ctx = {"request": request, "question": question_view.model_dump()}
    return templates.TemplateResponse("update_question.html", ctx)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=Response,
    response_model=None,
)
async def delete_question(question_id: int, db: Session = Depends(get_db)) -> None:
    await db_obj_delete(question_id, Question, "Question", db)


def validate_question_data(
    game_name: str,
    category: str,
    author: str,
    text: str,
    excluded: bool = False,
) -> QuestionSchema:
    try:
        question = QuestionSchema(
            game_name=game_name,
            category=category,
            author=author,
            text=text,
            excluded=excluded,
        )
    except ValueError:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data input")
    return question


def create_question_view(question: Question | Type[Question]) -> QuestionView:
    return QuestionView.model_validate(question)


def create_question_view_with_answers(
    question: Question | Type[Question],
) -> QuestionWithAnswersView:
    return QuestionWithAnswersView(
        id=question.id,  # type: ignore
        game_name=question.game_name,  # type: ignore
        category=question.category,  # type: ignore
        author=question.author,  # type: ignore
        text=question.text,  # type: ignore
        excluded=question.excluded,  # type: ignore
        answers=[AnswerView.model_validate(answer) for answer in question.answers],
    )
