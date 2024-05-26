from fastapi import Depends
from sqlmodel import Session

from domuwa import database as db
from domuwa.models.question import Question


async def get_question_by_id(
    question_id: int, db_sess: Session = Depends(db.get_db_session)
):
    return await db.get(question_id, Question, db_sess)
