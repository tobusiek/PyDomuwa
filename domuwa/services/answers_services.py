from logging import getLogger
from typing import Type

from fastapi import Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from domuwa.models import Answer, Question
from domuwa.schemas import AnswerSchema
from domuwa.database import db_obj_save, get_db, get_obj_of_type_by_id

logger = getLogger("db_connector")


async def create_answer(answer: AnswerSchema, db: Session = Depends(get_db)) -> Answer:
    question = await get_obj_of_type_by_id(answer.question_id, Question, "Question", db)
    if not question:
        raise HTTPException(status.HTTP_400_BAD_REQUEST, "Question not found")
    if answer.correct:
        await check_correct_answer_already_exists_for_question(question.id, db)
    db_answer = Answer(
        author=answer.author,
        text=answer.text,
        correct=answer.correct,
        question_id=answer.question_id,
        question=question
    )
    question.answers.append(db_answer)
    db.add(question)
    return await db_obj_save(db_answer, db)


async def get_answers_for_question(question_id: int, db: Session = Depends(get_db)) -> list[Type[Answer]]:
    return db.query(Answer).filter(Answer.question_id == question_id).all()


async def update_answer(answer_id: int, modified_answer: AnswerSchema, db: Session = Depends(get_db)) -> Type[Answer]:
    answer = await get_obj_of_type_by_id(answer_id, Answer, "Answer", db)
    if modified_answer.correct:
        await check_correct_answer_already_exists_for_question(answer.question_id, db)
    answer.author = modified_answer.author
    answer.text = modified_answer.text
    answer.correct = modified_answer.correct
    return await db_obj_save(answer, db)


async def check_correct_answer_already_exists_for_question(question_id: int, db: Session = Depends(get_db)) -> None:
    question = await get_obj_of_type_by_id(question_id, Question, "Question", db)
    correct_answer_in_question = any(answer for answer in question.answers if answer.correct)
    logger.debug(f"{question=} {correct_answer_in_question=}")
    if correct_answer_in_question:
        raise HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Correct answer already marked for question of id={question_id}, unmark earlier correct answer first")
