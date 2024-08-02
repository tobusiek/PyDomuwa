import logging

from fastapi import APIRouter, Depends
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

    @override
    async def create(
        self,
        create_model: AnswerCreate,
        session: Session = Depends(get_db_session),
    ):
        return await super().create(create_model, session)

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
