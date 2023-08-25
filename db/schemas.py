from pydantic import BaseModel


class PlayerBase(BaseModel):
    name: str


class PlayerCreate(PlayerBase):
    ...


class Player(PlayerBase):
    id: int
    score: int

    class Config:
        from_attributes = True


class AnswerBase(BaseModel):
    text: str
    points: int


class AnswerCreate(AnswerBase):
    ...


class AnswerUpdate(AnswerBase):
    ...


class Answer(AnswerBase):
    id: int
    question_id: int

    class Config:
        from_attributes = True


class QuestionBase(BaseModel):
    text: str


class QuestionCreate(QuestionBase):
    ...


class QuestionUpdate(QuestionBase):
    correct_answer_idx: int


class Question(QuestionBase):
    id: int
    answers: list[Answer] = []

    class Config:
        from_attributes = True


class GameBase(BaseModel):
    name: str


class GameCreate(GameBase):
    ...


class Game(GameBase):
    id: int
    players: list[Player] = []
    questions: list[Question] = []

    class Config:
        from_attributes = True
