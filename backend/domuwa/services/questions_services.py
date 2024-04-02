# def create_question(
#     question: schemas.QuestionCreateSchema,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> models.Question:
#     db_question = models.Question(
#         game_name=question.game_name,
#         category=question.category,
#         author=question.author,
#         text=question.text,
#     )
#     return db.save_obj(db_question, db_sess)
#
#
# def update_question(
#     question_id: int,
#     modified_question: schemas.QuestionCreateSchema,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> models.Question:
#     question = db.get_obj_of_type_by_id(
#         question_id,
#         models.Question,
#         "Question",
#         db_sess,
#     )
#     question.game_name = modified_question.game_name
#     question.category = modified_question.category
#     question.author = modified_question.author
#     question.text = modified_question.text
#     return db.save_obj(question, db_sess)
#
#
# def update_question_excluded(
#     question_id: int,
#     excluded: bool,
#     db_sess: Session = Depends(db.get_db_session),
# ) -> models.Question:
#     question = db.get_obj_of_type_by_id(
#         question_id,
#         models.Question,
#         "Question",
#         db_sess,
#     )
#     question.excluded = excluded
#     return db.save_obj(question, db_sess)
