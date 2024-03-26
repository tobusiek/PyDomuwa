from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from domuwa import database as db
from domuwa import logging
from domuwa.models.db_models import Answer, Question

logger = logging.get_logger("db_connector")


# def create_answer(
#     answer: schemas.AnswerCreateSchema,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> Answer:
#     if answer.question_id is None:
#         question = None
#     else:
#         question = db.get_obj_of_type_by_id(
#             answer.question_id,
#             Question,
#             "Question",
#             db_sess,
#         )
#
#     if answer.correct and answer.question_id is not None:
#         check_correct_answer_already_exists_for_question(answer.question_id, db_sess)
#
#     db_answer = Answer(
#         author=answer.author,
#         text=answer.text,
#         correct=answer.correct,
#         question_id=answer.question_id,
#         question=question,
#     )  # type: ignore
#
#     if question is not None:
#         question.answers.append(db_answer)
#         db_sess.add(question)
#
#     return db.save_obj(db_answer, db_sess)
#
#
# def get_answers_for_question(
#     question_id: int,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> list[Answer]:
#     return db_sess.query(Answer).filter(Answer.question_id == question_id).all()
#
#
# def update_answer(
#     answer_id: int,
#     modified_answer: schemas.AnswerCreateSchema,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> Answer:
#     answer = db.get_obj_of_type_by_id(answer_id, Answer, "Answer", db_sess)
#     if modified_answer.correct:
#         check_correct_answer_already_exists_for_question(
#             answer.question_id,  # type: ignore
#             db_sess,
#         )
#     answer.author = modified_answer.author
#     answer.text = modified_answer.text
#     answer.correct = modified_answer.correct
#     return db.save_obj(answer, db_sess)
#
#
# def check_correct_answer_already_exists_for_question(
#     question_id: int,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> None:
#     question = db.get_obj_of_type_by_id(
#         question_id,
#         Question,
#         "Question",
#         db_sess,
#     )
#     correct_answer_in_question = any(
#         answer for answer in question.answers if answer.correct
#     )
#     logger.debug(f"{question=} {correct_answer_in_question=}")
#     if correct_answer_in_question:
#         raise HTTPException(
#             status.HTTP_400_BAD_REQUEST,
#             f"Correct answer already marked for question of id={question_id}, unmark earlier correct answer first",
#         )
