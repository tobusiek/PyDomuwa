import fastapi
from sqlalchemy import orm
from starlette import status

from domuwa import database as db
from domuwa import models, schemas
from domuwa.utils import logging

logger = logging.get_logger("db_connector")


async def create_answer(
    answer: schemas.AnswerSchema,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Answer:
    question = await db.get_obj_of_type_by_id(
        answer.question_id,
        models.Question,
        "Question",
        db_sess,
    )
    if not question:
        raise fastapi.HTTPException(status.HTTP_400_BAD_REQUEST, "Question not found")
    if answer.correct:
        await check_correct_answer_already_exists_for_question(question.id, db_sess)
    db_answer = models.Answer(
        author=answer.author,
        text=answer.text,
        correct=answer.correct,
        question_id=answer.question_id,
        question=question,
    )  # type: ignore
    question.answers.append(db_answer)
    db_sess.add(question)
    return await db.db_obj_save(db_answer, db_sess)


async def get_answers_for_question(
    question_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> list[models.Answer]:
    return (
        db_sess.query(models.Answer)
        .filter(models.Answer.question_id == question_id)
        .all()
    )


async def update_answer(
    answer_id: int,
    modified_answer: schemas.AnswerSchema,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Answer:
    answer = await db.get_obj_of_type_by_id(answer_id, models.Answer, "Answer", db_sess)
    if modified_answer.correct:
        await check_correct_answer_already_exists_for_question(
            answer.question_id,
            db_sess,
        )
    answer.author = modified_answer.author
    answer.text = modified_answer.text
    answer.correct = modified_answer.correct
    return await db.db_obj_save(answer, db_sess)


async def check_correct_answer_already_exists_for_question(
    question_id: int,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> None:
    question = await db.get_obj_of_type_by_id(
        question_id,
        models.Question,
        "Question",
        db_sess,
    )
    correct_answer_in_question = any(
        answer for answer in question.answers if answer.correct
    )
    logger.debug(f"{question=} {correct_answer_in_question=}")
    if correct_answer_in_question:
        raise fastapi.HTTPException(
            status.HTTP_400_BAD_REQUEST,
            f"Correct answer already marked for question of id={question_id}, unmark earlier correct answer first",
        )
