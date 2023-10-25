import fastapi
import pydantic
from sqlalchemy import orm
from starlette import responses, status, templating

from domuwa import config, models, schemas
from domuwa import database as db
from domuwa.services import answers_services as services
from domuwa.utils import logging

logger = logging.get_logger("domuwa")

router = fastapi.APIRouter(prefix="/answer", tags=["Answer"])
templates = templating.Jinja2Templates(directory="resources/templates")


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=None)
async def create_answer(
    request: fastapi.Request,
    author: str,
    text: str,
    question_id: int,
    correct: bool = False,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.AnswerWithQuestionView | templating._TemplateResponse:
    answer_view = validate_answer_data(author, text, correct, question_id)
    logger.debug(f"{answer_view=}")
    db_answer = await services.create_answer(answer_view, db_sess)
    answer_view = create_answer_view_with_question(db_answer)
    if config.TESTING:
        return answer_view
    ctx = {"request": request, "answer": answer_view.model_dump()}
    return templates.TemplateResponse("create_answer.html", ctx)


@router.get("/{answer_id}", response_model=None)
async def get_answer_by_id(
    request: fastapi.Request,
    answer_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.AnswerWithQuestionView | templating._TemplateResponse:
    answer = await db.get_obj_of_type_by_id(answer_id, models.Answer, "Answer", db_sess)
    answer_view = create_answer_view_with_question(answer)
    if config.TESTING:
        return answer_view
    ctx = {"request": request, answer: answer_view.model_dump()}
    return templates.TemplateResponse("get_answer.html", ctx)


@router.get("/", response_model=None)
async def get_all_answers(
    request: fastapi.Request,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> list[schemas.AnswerWithQuestionView] | templating._TemplateResponse:
    answers = await db.get_all_objs_of_type(models.Answer, db_sess)
    answer_views = [create_answer_view_with_question(answer) for answer in answers]
    if config.TESTING:
        return answer_views
    ctx = {
        "request": request,
        "answers": [answer_view.model_dump() for answer_view in answer_views],
    }
    return templates.TemplateResponse("get_all_answers.html", ctx)


@router.get("/for_question/{question_id}", response_model=None)
async def get_answers_for_question(
    request: fastapi.Request,
    question_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> list[schemas.AnswerView] | templating._TemplateResponse:
    answers = await services.get_answers_for_question(question_id, db_sess)
    answer_views = [create_answer_view(answer) for answer in answers]
    if config.TESTING:
        return answer_views
    ctx = {
        "request": request,
        "answers": [answer_view.model_dump() for answer_view in answer_views],
    }
    return templates.TemplateResponse("get_answers_for_question.html", ctx)


@router.put("/", response_model=None)
async def update_answer(
    request: fastapi.Request,
    answer_id: int,
    author: str,
    text: str,
    correct: bool,
    question_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> schemas.AnswerWithQuestionView | templating._TemplateResponse:
    modified_answer = validate_answer_data(author, text, correct, question_id)
    answer = await services.update_answer(answer_id, modified_answer, db_sess)
    answer_view = create_answer_view_with_question(answer)
    if config.TESTING:
        return answer_view
    ctx = {"request": request, "answer": answer_view.model_dump()}
    return templates.TemplateResponse("update_answer.html", ctx)


@router.delete(
    "/", status_code=status.HTTP_204_NO_CONTENT, response_class=responses.Response,
)
async def delete_answer(
    answer_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> None:
    await db.db_obj_delete(answer_id, models.Answer, "Answer", db_sess)


def validate_answer_data(
    author: str,
    text: str,
    correct: bool,
    question_id: int,
) -> schemas.AnswerSchema:
    try:
        answer = schemas.AnswerSchema(
            author=author,
            text=text,
            correct=correct,
            question_id=question_id,
        )
    except pydantic.ValidationError:
        raise fastapi.HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data input")
    return answer


def create_answer_view(answer: models.Answer) -> schemas.AnswerView:
    return schemas.AnswerView.model_validate(answer)


def create_answer_view_with_question(
    answer: models.Answer,
) -> schemas.AnswerWithQuestionView:
    return schemas.AnswerWithQuestionView(
        id=answer.id,
        author=answer.author,
        text=answer.text,
        correct=answer.correct,
        question_id=answer.question_id,
        question=schemas.QuestionView.model_validate(answer.question),
    )  # type: ignore
