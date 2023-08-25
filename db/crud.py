from typing import Type

from fastapi import HTTPException
from sqlalchemy.orm import Session

import db.models as models
import db.schemas as schemas


def get_active_games(db: Session) -> list[Type[models.Game]]:
    return db.query(models.Game).all()


def create_game(db: Session, game: schemas.GameCreate) -> models.Game:
    db_game = models.Game(name=game.name)
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def get_game_by_id(db: Session, game_id: int):
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def add_player_to_game(db: Session, game_id: int, player: schemas.PlayerCreate) -> models.Player:
    db_game = db.query(models.Game).filter(models.Game.id == game_id).first()
    if not db_game:
        raise HTTPException(status_code=404, detail="Game not found")

    db_player = models.Player(**player.model_dump())
    db_game.players.append(db_player)
    db.commit()
    db.refresh(db_game)
    return db_player


def create_player(db: Session, player: schemas.PlayerCreate) -> models.Player:
    db_player = models.Player(name=player.name)
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def get_player_by_nickname(db: Session, nickname: str):
    return db.query(models.Player).filter(models.Player.name == nickname).first()


def update_question(db: Session, question_id: int, question: schemas.QuestionUpdate):
    db_question = db.query(models.Question).filter(models.Question.id == question_id).first()
    if not db_question:
        raise HTTPException(status_code=404, detail="Question not found")

    for key, value in question.model_dump().items():
        setattr(db_question, key, value)

    db.commit()
    db.refresh(db_question)
    return db_question


def update_answer(db: Session, answer_id: int, answer: schemas.AnswerUpdate):
    db_answer = db.query(models.Answer).filter(models.Answer.id == answer_id).first()
    if not db_answer:
        raise HTTPException(status_code=404, detail="Answer not found")

    for key, value in answer.model_dump().items():
        setattr(db_answer, key, value)

    db.commit()
    db.refresh(db_answer)
    return db_answer
