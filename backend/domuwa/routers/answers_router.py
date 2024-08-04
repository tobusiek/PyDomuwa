import logging

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing_extensions import override

from domuwa.database import get_db_session
from domuwa.models.answer import Answer, AnswerCreate, AnswerRead, AnswerUpdate
from domuwa.routers.common_router import CommonRouter
from domuwa.services.answers_services import AnswerServices


class AnswerRouter(CommonRouter[AnswerCreate, AnswerUpdate, Answer]):
    prefix = "/answers"
    tags = ["Answer"]
    response_model = AnswerRead
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    services = AnswerServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = Answer.__name__

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
            response_model=AnswerRead,
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

        err_msg = f"Got Answer(id={model_id}) to get, but it was deleted"
        self.logger.warning(err_msg)
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)

    @override
    async def create(
        self,
        model: AnswerCreate,
        session: Session = Depends(get_db_session),
    ):
        return await super().create(model, session)

    @override
    async def update(
        self,
        model_id: int,
        model_update: AnswerUpdate,
        session: Session = Depends(get_db_session),
    ):
        return await super().update(model_id, model_update, session)


def get_answers_router():
    return AnswerRouter().router
