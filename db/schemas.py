from typing import List
from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    pass


class Player(PlayerBase):
    id: int
    score: int

    class Config:
        orm_mode = True


class QuestionBase(BaseModel):
    text: str


class QuestionCreate(QuestionBase):
    pass


class QuestionUpdate(QuestionBase):
    correct_answer_idx: int


class Question(QuestionBase):
    id: int
    answers: List["Answer"] = []

    class Config:
        orm_mode = True


class AnswerBase(BaseModel):
    text: str
    points: int


class AnswerCreate(AnswerBase):
    pass


class AnswerUpdate(AnswerBase):
    pass


class Answer(AnswerBase):
    id: int
    question_id: int

    class Config:
        orm_mode = True


class GameBase(BaseModel):
    name: str


class GameCreate(GameBase):
    pass


class Game(GameBase):
    id: int
    players: List[Player] = []
    questions: List[Question] = []

    class Config:
        orm_mode = True
