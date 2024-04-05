import logging

from fastapi import Depends, HTTPException, status
from sqlalchemy.exc import IntegrityError
from sqlmodel import Session

from domuwa import database as db
from domuwa.models.db_models import QnACategory

logger = logging.getLogger(__name__)


async def create_qna_category(
    qna_category: QnACategory, db_sess: Session = Depends(db.get_db_session)
):
    try:
        db_qna_category = await db.save(qna_category, db_sess)
    except IntegrityError as exc:
        logger.error(str(exc))
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST, "QnACategory of given name already exists"
        ) from exc
    return db_qna_category
