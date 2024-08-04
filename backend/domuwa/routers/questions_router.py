import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing_extensions import override

from domuwa.database import get_db_session
from domuwa.models.question import (
    Question,
    QuestionCreate,
    QuestionRead,
    QuestionUpdate,
    QuestionWithAnswersRead,
)
from domuwa.routers.common_router import CommonRouter
from domuwa.services.questions_services import QuestionServices


class QuestionRouter(CommonRouter[QuestionCreate, QuestionUpdate, Question]):
    prefix = "/questions"
    tags = ["Question"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = QuestionWithAnswersRead
    services = QuestionServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = Question.__name__

    def __init__(self) -> None:
        super().__init__()

        self.router.routes.remove(
            next(route for route in self.router.routes if route.name == "create")  # type: ignore
        )
        self.router.add_api_route(
            "/",
            self.create,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
            response_model=QuestionRead,
        )

    @override
    async def get_by_id(
        self,
        model_id: int,
        session: Session = Depends(get_db_session),
    ):
        model = await super().get_by_id(model_id, session)
        if not model.deleted:
            return model

        err_msg = f"Got Question(id={model_id}) to get, but it was deleted"
        self.logger.warning(err_msg)
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)

    @override
    async def create(
        self,
        model: QuestionCreate,
        session: Session = Depends(get_db_session),
    ):
        return await super().create(model, session)

    @override
    async def update(
        self,
        model_id: int,
        model_update: QuestionUpdate,
        session: Session = Depends(get_db_session),
    ):
        return await super().update(model_id, model_update, session)


def get_questions_router():
    return QuestionRouter().router
