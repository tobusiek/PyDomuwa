from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from domuwa.database import db_obj_save, get_db, get_obj_of_type_by_id
from domuwa.models import Question
from domuwa.schemas import QuestionSchema


async def create_question(
    question: QuestionSchema, db: Session = Depends(get_db)
) -> Question:
    db_question = Question(
        game_name=question.game_name,
        category=question.category,
        author=question.author,
        text=question.text,
    )  # type: ignore
    return await db_obj_save(db_question, db)


async def update_question(
    question_id: int,
    modified_question: QuestionSchema,
    db: Session = Depends(get_db),
) -> Type[Question]:
    question = await get_obj_of_type_by_id(question_id, Question, "Question", db)
    question.game_name = modified_question.game_name
    question.category = modified_question.category
    question.author = modified_question.author
    question.text = modified_question.text
    return await db_obj_save(question, db)


async def update_question_excluded(
    question_id: int,
    excluded: bool,
    db: Session = Depends(get_db),
) -> Question:
    question = await get_obj_of_type_by_id(question_id, Question, "Question", db)
    question.excluded = excluded
    return await db_obj_save(question, db)
