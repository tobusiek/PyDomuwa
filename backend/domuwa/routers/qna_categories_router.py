import logging

from fastapi import Depends, HTTPException, status
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
from domuwa.routers.common_router import CommonRouter
from domuwa.services.qna_categories_services import QnACategoryServices


class QnACategoriesRouter(
    CommonRouter[QnACategoryCreate, QnACategoryUpdate, QnACategory]
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
        create_model: QnACategoryCreate,
        session: Session = Depends(get_db_session),
    ):
        qna_category = await super().create(create_model, session)
        if qna_category is None:
            err_msg = f"QnACategory({create_model}) could not be created."
            self.logger.warning(err_msg)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, err_msg)
        return qna_category

    # TODO: add admin auth
    @override
    async def update(
        self,
        model_id: int,
        model_update: QnACategoryUpdate,
        session: Session = Depends(get_db_session),
    ):
        qna_category = await super().update(model_id, model_update, session)
        if qna_category is None:
            err_msg = f"QnACategory({model_update}) could not be created."
            self.logger.warning(err_msg)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, err_msg)
        return qna_category


def get_qna_categories_router():
    return QnACategoriesRouter().router
