from fastapi import HTTPException
from sqlalchemy.orm import Session

import db.schemas as schemas
from .models.answer import Answer
from .models.game import Game
from .models.player import Player
from .models.question import Question


def create_game(db: Session, game: schemas.GameCreate):
    db_game = Game(name=game.name)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def add_player_to_game(db: Session, game_id: int, player: schemas.PlayerCreate):
    db_game = db.query(Game).filter(Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    db_player = Player(**player.model_dump())
    db_game.players.append(db_player)
    db.commit()
    db.refresh(db_game)
    return db_player


def update_question(db: Session, question_id: int, question: schemas.QuestionUpdate):
    db_question = db.query(Question).filter(Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    for key, value in question.model_dump().items():
        setattr(db_question, key, value)

    db.commit()
    db.refresh(db_question)
    return db_question


def update_answer(db: Session, answer_id: int, answer: schemas.AnswerUpdate):
    db_answer = db.query(Answer).filter(Answer.id == answer_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    for key, value in answer.model_dump().items():
        setattr(db_answer, key, value)

    db.commit()
    db.refresh(db_answer)
    return db_answer
