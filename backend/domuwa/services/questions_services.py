import fastapi
from sqlalchemy import orm

from domuwa import database as db
from domuwa import models, schemas


async def create_question(
    question: schemas.QuestionSchema,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Question:
    db_question = models.Question(
        game_name=question.game_name,
        category=question.category,
        author=question.author,
        text=question.text,
    )
    return await db.save_obj(db_question, db_sess)


async def update_question(
    question_id: int,
    modified_question: schemas.QuestionSchema,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Question:
    question = await db.get_obj_of_type_by_id(
        question_id,
        models.Question,
        "Question",
        db_sess,
    )
    question.game_name = modified_question.game_name
    question.category = modified_question.category
    question.author = modified_question.author
    question.text = modified_question.text
    return await db.save_obj(question, db_sess)


async def update_question_excluded(
    question_id: int,
    excluded: bool,
    db_sess: orm.Session = fastapi.Depends(db.get_db_session),
) -> models.Question:
    question = await db.get_obj_of_type_by_id(
        question_id,
        models.Question,
        "Question",
        db_sess,
    )
    question.excluded = excluded
    return await db.save_obj(question, db_sess)
