from db.models.answer import Answer
from db.models.game import Game
from db.models.player import Player
from db.models.question import Question


def initialize_tables():
    Game.delete_all()
    Game.create_table()
    Player.create_table()
    Question.create_table()
    Answer.create_table()


def create_constraints():
    Player.create_index()
    Player.create_foreign_key(Game.table_name)
    Question.create_index()
    Question.create_foreign_key(Answer.table_name)
    Answer.create_foreign_key(Question.table_name)


def get_active_games() -> list[Game]:
    return Game.get_all()


def create_game(name: str, category: str, rounds: int) -> Game:
    db_game = Game(name, category=category, rounds=rounds)
    db_game.save()
    return db_game


def get_game_by_id(game_id: int) -> Game | None:
    return Game.get_by_id(game_id)


def create_player(nickname: str) -> Player:
    db_player = Player(nickname)
    db_player.save()
    return db_player


def get_player_by_id(player_id: int) -> Player | None:
    return Player.get_by_id(player_id)


def get_player_by_nickname(nickname: str) -> Player | None:
    return Player.get_by_name(nickname)


def get_questions_for_game(game_name: str, game_category: str) -> list[Question]:
    return Question.get_by_game_type(game_name, game_category)

# def update_question(question_id: int, question: schemas.QuestionUpdate):
#     db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
#     if not db_question:
#         raise HTTPException(status_code=404, detail="Question not found")
#
#     for key, value in question.model_dump().items():
#         setattr(db_question, key, value)
#
#     db.commit()
#     db.refresh(db_question)
#     return db_question
#
#
# def update_answer(answer_id: int, answer: schemas.AnswerUpdate):
#     db_answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
#     if not db_answer:
#         raise HTTPException(status_code=404, detail="Answer not found")
#
#     for key, value in answer.model_dump().items():
#         setattr(db_answer, key, value)
#
#     db.commit()
#     db.refresh(db_answer)
#     return db_answer
