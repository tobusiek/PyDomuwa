import logging

from fastapi import Depends
from sqlmodel import Session

from domuwa import database as db
from domuwa.models.qna_category import QnACategory

logger = logging.getLogger(__name__)


async def create_qna_category(
    qna_category: QnACategory,
    db_sess: Session = Depends(db.get_db_session),
):
    return await db.save(qna_category, db_sess)


async def get_qna_category_by_id(
    qna_category_id: int,
    db_sess: Session = Depends(db.get_db_session),
):
    return await db.get(qna_category_id, QnACategory, db_sess)


async def get_all_qna_categories(db_sess: Session = Depends(db.get_db_session)):
    return await db.get_all(QnACategory, db_sess)


async def update_qna_category(
    qna_category_id: int,
    qna_category: QnACategory,
    db_sess: Session = Depends(db.get_db_session),
):
    return await db.update(qna_category_id, qna_category, db_sess)


async def delete_qna_category(
    qna_category_id: int,
    db_sess: Session = Depends(db.get_db_session),
):
    await db.delete(qna_category_id, QnACategory, db_sess)
