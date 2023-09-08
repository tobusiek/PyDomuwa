from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from domuwa.answer.model import Answer
from domuwa.answer.schema import AnswerCreate
from domuwa.database import db_obj_save, get_db, get_obj_of_type_by_id


async def create_answer(answer: AnswerCreate, db: Session = Depends(get_db)) -> Answer:
    db_answer = Answer(
        author=answer.author,
        text=answer.text,
        points=answer.points,
        correct=answer.correct,
        question_id=answer.question_id,
    )
    return await db_obj_save(db_answer, db)


async def get_answers_for_question(question_id: int, db: Session = Depends(get_db)) -> list[Type[Answer]]:
    return db.query(Answer).filter(Answer.question_id == question_id).all()


async def update_answer(answer_id: int, modified_answer: AnswerCreate, db: Session = Depends(get_db)) -> Type[Answer]:
    answer = await get_obj_of_type_by_id(answer_id, Answer, "Answer", db)
    answer.author = modified_answer.author
    answer.text = modified_answer.text
    answer.points = modified_answer.points
    answer.correct = modified_answer.correct
    return await db_obj_save(answer, db)
