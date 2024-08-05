import logging

from fastapi import Depends
from fastapi.routing import APIRouter
from sqlmodel import Session
from typing_extensions import override

from domuwa.database import get_db_session
from domuwa.models.qna_category import (
    QnACategory,
    QnACategoryCreate,
    QnACategoryRead,
    QnACategoryUpdate,
)
from domuwa.routers.common_router import CommonRouter400OnSaveError
from domuwa.services.qna_categories_services import QnACategoryServices


class QnACategoriesRouter(
    CommonRouter400OnSaveError[QnACategoryCreate, QnACategoryUpdate, QnACategory]
):
    prefix = "/qna-categories"
    tags = ["QnA Category"]
    router = APIRouter(prefix=prefix, tags=tags)  # type: ignore
    response_model = QnACategoryRead
    services = QnACategoryServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = QnACategory.__name__

    # TODO: add admin auth
    @override
    async def create(
        self,
        model: QnACategoryCreate,
        session: Session = Depends(get_db_session),
    ):
        return await super().create(model, session)

    # TODO: add admin auth
    @override
    async def update(
        self,
        model_id: int,
        model_update: QnACategoryUpdate,
        session: Session = Depends(get_db_session),
    ):
        return await super().update(model_id, model_update, session)

    # TODO: add admin auth
    @override
    async def delete(self, model_id: int, session: Session = Depends(get_db_session)):
        return await super().delete(model_id, session)


def get_qna_categories_router():
    return QnACategoriesRouter().router
