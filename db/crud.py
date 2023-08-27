import db.schemas as schemas
from db.models.answer import Answer
from db.models.game import Game
from db.models.player import Player
from db.models.question import Question


def initialize_tables():
    Game.create_table()
    Player.create_table()
    Question.create_table()
    Answer.create_table()


def get_active_games() -> list[Game]:
    return Game.get_all()


def create_game(game: schemas.GameCreate) -> Game:
    db_game = Game(name=game.name)
    db_game.save()
    return db_game


def get_game_by_id(game_id: int):
    return Game.get_by_id(game_id)


# def add_player_to_game(game_id: int, player: schemas.PlayerCreate) -> models.Player:
#     db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
#     if not db_game:
#         raise HTTPException(status_code=404, detail="Game not found")
#
#     db_player = models.Player(**player.model_dump())
#     db_game.players.append(db_player)
#     db.commit()
#     db.refresh(db_game)
#     return db_player


def create_player(nickname: str) -> Player:
    db_player = Player(nickname)
    db_player.save()
    return db_player


def get_player_by_nickname(nickname: str) -> Player | None:
    return Player.get_by_name(nickname)

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
