from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from domuwa.database import db_obj_save, get_db, get_obj_of_type_by_id
from domuwa.question.model import Question
from domuwa.question.schema import QuestionCreate


async def create_question(question: QuestionCreate, db: Session = Depends(get_db)) -> Question:
    db_question = Question(
        game_name=question.game_name,
        category=question.category,
        author=question.author,
        text=question.text,
    )
    return await db_obj_save(db_question, db)


async def update_question(
        question_id: int,
        modified_question: QuestionCreate,
        db: Session = Depends(get_db)
) -> Type[Question]:
    question = await get_obj_of_type_by_id(question_id, Question, "Question", db)
    question.game_name = modified_question.game_name
    question.category = modified_question.category
    question.author = modified_question.author
    question.text = modified_question.text
    return await db_obj_save(question, db)
