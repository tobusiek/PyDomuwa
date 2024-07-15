import logging

from fastapi import Depends, HTTPException, status
from sqlmodel import Session

from domuwa import database as db
from domuwa.models.question import Question, QuestionUpdate

logger = logging.getLogger(__name__)


async def create_question(
    question: Question,
    db_sess: Session = Depends(db.get_db_session),
):
    return await db.save(question, db_sess)


async def get_question_by_id(
    question_id: int,
    db_sess: Session = Depends(db.get_db_session),
):
    question = await db.get(question_id, Question, db_sess)
    if not question.deleted:
        return question

    err_msg = f"Got Question(id={question_id}) to get, but it was deleted"
    logger.warning(err_msg)
    raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)


async def get_all_questions(db_sess: Session = Depends(db.get_db_session)):
    return await db.get_all(Question, db_sess)


async def update_question(
    question_update: QuestionUpdate,
    question: Question,
    db_sess: Session = Depends(db.get_db_session),
):
    question_update_data = question_update.model_dump(exclude_unset=True)
    for field, value in question_update_data.items():
        setattr(question, field, value)

    old_question = await db.get(question.id, Question, db_sess)
    question.prev_version = old_question

    answers = old_question.answers
    if answers:
        question.answers = answers

    db_sess.add(question)
    db_sess.commit()
    db_sess.refresh(question)
    return question


async def delete_question(
    question_id: int,
    db_sess: Session = Depends(db.get_db_session),
):
    question = await db.get(question_id, Question, db_sess)
    question.deleted = True

    for answer in question.answers:
        answer.deleted = True
        db_sess.add(answer)

    db_sess.add(question)
    db_sess.commit()
