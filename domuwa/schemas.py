from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, ValidationError, field_validator


class AnswerSchema(BaseModel):
    author: str
    text: str
    correct: bool = False
    question_id: int


class AnswerView(AnswerSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class QuestionSchema(BaseModel):
    game_name: str
    category: str
    author: str
    text: str
    excluded: bool = False


class QuestionView(QuestionSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class QuestionWithAnswersView(QuestionView):
    answers: list[AnswerView]


class AnswerWithQuestionView(AnswerView):
    question: QuestionView


class GameCategory(Enum):
    SFW = "SFW"
    NSFW = "NSFW"
    MIXED = "MIXED"


class GameRoomSchema(BaseModel):
    game_name: str
    game_category: str

    @field_validator("game_category")
    @classmethod
    def check_category(cls, category: str) -> str:
        if category not in [game_cat.value for game_cat in GameCategory]:
            raise ValidationError(f"Invalid {category=}")
        return category


class GameRoomView(GameRoomSchema):
    id: int
    model_config = ConfigDict(from_attributes=True)


class PlayerSchema(BaseModel):
    name: str


class PlayerView(PlayerSchema):
    id: int
    game_rooms_played: int
    game_rooms_won: int
    score: float
    model_config = ConfigDict(from_attributes=True)


class PlayerWithGameView(PlayerView):
    game: Optional[GameRoomView]


class GameRoomWithPlayersView(GameRoomView):
    players: list[PlayerView]
