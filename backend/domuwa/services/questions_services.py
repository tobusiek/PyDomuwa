from fastapi import Depends
from sqlmodel import Session

from domuwa import database as db
from domuwa.models.question import Question


async def create_question(
    question: Question,
    db_sess: Session = Depends(db.get_db_session),
):
    raise NotImplementedError()


async def get_question_by_id(
    question_id: int,
    db_sess: Session = Depends(db.get_db_session),
):
    return await db.get(question_id, Question, db_sess)


async def get_all_questions(db_sess: Session = Depends(db.get_db_session)):
    raise NotImplementedError()


async def update_question(
    question_id: int,
    question: Question,
    db_sess: Session = Depends(db.get_db_session),
):
    raise NotImplementedError()


async def delete_question(
    question_id: int,
    db_sess: Session = Depends(db.get_db_session),
):
    raise NotImplementedError()
