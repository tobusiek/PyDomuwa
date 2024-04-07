import logging

from fastapi import Depends, HTTPException, status
from fastapi.routing import APIRouter
from pydantic import ValidationError
from sqlmodel import Session

from domuwa.database import get_db_session
from domuwa.models.qna_category import (
    QnACategory,
    QnACategoryCreate,
    QnACategoryRead,
    QnACategoryUpdate,
)
from domuwa.services import qna_categories_services as services

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/qna-categories", tags=["QnA Categories"])


@router.post("/", response_model=QnACategoryRead, status_code=status.HTTP_201_CREATED)
async def create_qna_category(
    qna_category_create: QnACategoryCreate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        logger.debug("received QnACategory(%s) to create", qna_category_create)
        qna_category = QnACategory.model_validate(qna_category_create, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Provided invalid data")

    return await services.create_qna_category(qna_category, db_sess)


@router.get("/{qna_category_id}", response_model=QnACategoryRead)
async def get_qna_category_by_id(
    qna_category_id: int,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug("received QnACategory(id=%d) to get", qna_category_id)
    return await services.get_qna_category_by_id(qna_category_id, db_sess)


@router.get("/", response_model=list[QnACategoryRead])
async def get_all_qna_categories(db_sess: Session = Depends(get_db_session)):
    return await services.get_all_qna_categories(db_sess)


@router.patch("/{qna_category_id}", response_model=QnACategoryRead)
async def update_qna_category(
    qna_category_id: int,
    qna_category_update: QnACategoryUpdate,
    db_sess: Session = Depends(get_db_session),
):
    try:
        logger.debug(
            "received QnACategory(%s) to update QnACategory(id=%d)",
            qna_category_update,
            qna_category_id,
        )
        qna_category = QnACategory.model_validate(qna_category_update, strict=True)
    except ValidationError as exc:
        logger.error(str(exc))
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Provided invalid data")

    return await services.update_qna_category(qna_category_id, qna_category, db_sess)


@router.delete("/{qna_category_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_qna_category(
    qna_category_id: int,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug("received QnACategory(id=%d) to delete", qna_category_id)
    await services.delete_qna_category(qna_category_id, db_sess)
