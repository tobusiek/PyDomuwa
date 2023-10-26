import fastapi
import pydantic
from fastapi import status
from sqlalchemy import orm
from starlette import templating

from domuwa import config, models, schemas
from domuwa import database as db
from domuwa.services import questions_services as services
from domuwa.utils import logging

logger = logging.get_logger("domuwa")

router = fastapi.APIRouter(prefix="/question", tags=["Question"])
templates = templating.Jinja2Templates(directory="resources/templates")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_question(
    request: fastapi.Request,
    game_name: str,
    category: str,
    author: str,
    text: str,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.QuestionView | templating._TemplateResponse:
    question = validate_question_data(game_name, category, author, text)
    db_question = await services.create_question(question, db_sess)
    question_view = create_question_view(db_question)
    if config.TESTING:
        return question_view
    ctx = {"request": request, "question": question_view.model_dump()}
    return templates.TemplateResponse("create_question.html", ctx)


@router.get("/{question_id}", response_model=None)
async def get_question_by_id(
    request: fastapi.Request,
    question_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.QuestionWithAnswersView | templating._TemplateResponse:
    question = await db.get_obj_of_type_by_id(
        question_id, models.Question, "Question", db_sess,
    )
    question_view = create_question_view_with_answers(question)
    if config.TESTING:
        return question_view
    ctx = {"request": request, "question": question_view.model_dump()}
    return templates.TemplateResponse("get_question.html", ctx)


@router.get("/", response_model=None)
async def get_all_questions(
    request: fastapi.Request,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> list[schemas.QuestionWithAnswersView] | templating._TemplateResponse:
    questions = await db.get_all_objs_of_type(models.Question, db_sess)
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
    request: fastapi.Request,
    question_id: int,
    game_name: str,
    category: str,
    author: str,
    text: str,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.QuestionView | templating._TemplateResponse:
    modified_question = validate_question_data(game_name, category, author, text)
    db_question = await services.update_question(
        question_id, modified_question, db_sess,
    )
    question_view = create_question_view(db_question)
    if config.TESTING:
        return question_view
    ctx = {"request": request, "question": question_view.model_dump()}
    return templates.TemplateResponse("update_question.html", ctx)


@router.put("/excluding", response_model=None)
async def update_question_excluded(
    request: fastapi.Request,
    question_id: int,
    excluded: bool,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.QuestionView | templating._TemplateResponse:
    question = await services.update_question_excluded(question_id, excluded, db_sess)
    question_view = create_question_view(question)
    if config.TESTING:
        return question_view
    ctx = {"request": request, "question": question_view.model_dump()}
    return templates.TemplateResponse("update_question.html", ctx)


@router.delete(
    "/",
    status_code=status.HTTP_204_NO_CONTENT,
    response_class=fastapi.Response,
)
async def delete_question(
    question_id: int, db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> None:
    await db.delete_obj(question_id, models.Question, "Question", db_sess)


def validate_question_data(
    game_name: str,
    category: str,
    author: str,
    text: str,
    excluded: bool = False,
) -> schemas.QuestionSchema:
    try:
        question = schemas.QuestionSchema(
            game_name=game_name,
            category=category,
            author=author,
            text=text,
            excluded=excluded,
        )
    except pydantic.ValidationError:
        raise fastapi.HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data input")
    return question


def create_question_view(question: models.Question) -> schemas.QuestionView:
    return schemas.QuestionView.model_validate(question)


def create_question_view_with_answers(
    question: models.Question,
) -> schemas.QuestionWithAnswersView:
    return schemas.QuestionWithAnswersView(
        id=question.id,
        game_name=question.game_name,
        category=question.category,
        author=question.author,
        text=question.text,
        excluded=question.excluded,
        answers=[
            schemas.AnswerView.model_validate(answer) for answer in question.answers
        ],
    )
