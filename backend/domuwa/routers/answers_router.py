import logging

from fastapi import APIRouter

logger = logging.getLogger("domuwa")

router = APIRouter(prefix="/answer", tags=["Answer"])

# @router.post("/", status_code=status.HTTP_201_CREATED)
# async def create_answer(
#     request: Request,
#     author: str,
#     text: str,
#     question_id: int | None = None,
#     correct: bool = False,
#     db_sess: Session = Depends(db.get_db_session),
# ):
#     answer_view = validate_answer_data(author, text, correct, question_id)
#     logger.debug(f"{answer_view=}")
#     db_answer = services.create_answer(answer_view, db_sess)
#     return create_answer_view_with_question(db_answer)
#
#
# @router.get("/{answer_id}")
# def get_answer_by_id(
#     request: Request,
#     answer_id: int,
#     db_sess: Session = Depends(db.get_db_session),
# ):
#     answer = db.get_obj_of_type_by_id(answer_id, Answer, "Answer", db_sess)
#     return create_answer_view_with_question(answer)
#
#
# @router.get("/")
# def get_all_answers(request: Request, db_sess: Session = Depends(db.get_db_session)):
#     answers = db.get_all_objs_of_type(Answer, db_sess)
#     return [create_answer_view_with_question(answer) for answer in answers]
#
#
# @router.get("/for_question/{question_id}", response_model=None)
# def get_answers_for_question(
#     request: Request,
#     question_id: int,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> list[schemas.AnswerSchema]:
#     answers = services.get_answers_for_question(question_id, db_sess)
#     return [create_answer_view(answer) for answer in answers]
#
#
# @router.put("/", response_model=None)
# def update_answer(
#     request: Request,
#     answer_id: int,
#     author: str,
#     text: str,
#     correct: bool,
#     question_id: int,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> schemas.AnswerWithQuestionSchema:
#     modified_answer = validate_answer_data(author, text, correct, question_id)
#     answer = services.update_answer(answer_id, modified_answer, db_sess)
#     return create_answer_view_with_question(answer)
#
#
# @router.delete(
#     "/",
#     status_code=status.HTTP_204_NO_CONTENT,
#     response_class=responses.Response,
# )
# def delete_answer(
#     answer_id: int,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> None:
#     db.delete_obj(answer_id, Answer, "Answer", db_sess)
#
#
# def validate_answer_data(
#     author: str,
#     text: str,
#     correct: bool,
#     question_id: int | None = None,
# ) -> schemas.AnswerCreateSchema:
#     try:
#         answer = schemas.AnswerCreateSchema(
#             author=author,
#             text=text,
#             correct=correct,
#             question_id=question_id,
#         )
#     except ValidationError:
#         raise HTTPException(status.HTTP_400_BAD_REQUEST, "Invalid data input")
#     return answer
#
#
# def create_answer_view(answer: Answer) -> schemas.AnswerSchema:
#     return schemas.AnswerSchema.model_validate(answer)
#
#
# def create_answer_view_with_question(
#     answer: Answer,
# ) -> schemas.AnswerWithQuestionSchema:
#     return schemas.AnswerWithQuestionSchema(
#         id=answer.id,
#         author=answer.author,
#         text=answer.text,
#         correct=answer.correct,
#         question_id=answer.question_id,
#         question=schemas.QuestionSchema.model_validate(answer.question),
#     )  # type: ignore
