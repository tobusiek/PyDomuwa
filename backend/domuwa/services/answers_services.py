from fastapi import Depends
from sqlmodel import Session

from domuwa import database as db
from domuwa.models.answer import Answer


async def create_answer(answer: Answer, db_sess: Session = Depends(db.get_db_session)):
    return await db.save(answer, db_sess)


async def get_answer_by_id(
    answer_id: int,
    db_sess: Session = Depends(db.get_db_session),
):
    return await db.get(answer_id, Answer, db_sess)


async def get_all_answers(db_sess: Session = Depends(db.get_db_session)):
    return await db.get_all(Answer, db_sess)


async def update_answer(
    answer_id: int,
    answer: Answer,
    db_sess: Session = Depends(db.get_db_session),
):
    old_answer = await db.get(answer_id, Answer, db_sess)
    answer.prev_version = old_answer
    old_answer.next_versions.append(answer)

    question = old_answer.question
    if question is not None:
        question.answers.remove(old_answer)
        question.answers.append(answer)
        db_sess.add(question)

    db_sess.add(answer)
    db_sess.add(old_answer)
    db_sess.commit()
    db_sess.refresh(answer)
    return answer


async def delete_answer(answer_id: int, db_sess: Session = Depends(db.get_db_session)):
    answer = await db.get(answer_id, Answer, db_sess)

    question = answer.question
    if question is not None:
        question.answers.remove(answer)
        db_sess.add(question)

    db_sess.add(question)
    db_sess.commit()
