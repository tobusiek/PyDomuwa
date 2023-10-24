from enum import Enum
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, ValidationError, field_validator

from domuwa.utils.logging import get_logger

logger = get_logger("validator")

MIN_ID = 1
MIN_PLAYER_NAME_LEN = 3
MAX_PLAYER_NAME_LEN = 25
MIN_TEXT_LEN = 1
MAX_TEXT_LEN = 150

valid_id = Field(ge=1)


class AnswerSchema(BaseModel):
    author: str = Field(min_length=MIN_PLAYER_NAME_LEN, max_length=MAX_PLAYER_NAME_LEN)
    text: str = Field(min_length=MIN_TEXT_LEN, max_length=MAX_TEXT_LEN)
    correct: bool = Field(False)
    question_id: int = Field(strict=True, ge=MIN_ID)


class AnswerView(AnswerSchema):
    id: int = valid_id
    model_config = ConfigDict(from_attributes=True)


MIN_GAME_NAME_LEN = 3
MAX_GAME_NAME_LEN = 15
MIN_CATEGORY_LEN = 3
MAX_CATEGORY_LEN = 25


class QuestionSchema(BaseModel):
    game_name: str = Field(min_length=MIN_GAME_NAME_LEN, max_length=MAX_GAME_NAME_LEN)
    category: str = Field(min_length=MIN_CATEGORY_LEN, max_length=MAX_CATEGORY_LEN)
    author: str = Field(min_length=MIN_PLAYER_NAME_LEN, max_length=MAX_PLAYER_NAME_LEN)
    text: str = Field(min_length=MIN_TEXT_LEN, max_length=MAX_TEXT_LEN)
    excluded: bool = Field(False)

    @field_validator("game_name", mode="before")
    @classmethod
    def check_game_name(cls, game_name: str) -> str:
        if game_name not in ("ego", "who's-most-likely"):
            logger.warning("Invalid data")
            raise ValidationError(f"Invalid game name={game_name}")
        logger.info("valid data")
        return game_name


class QuestionView(QuestionSchema):
    id: int = valid_id
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
    game_name: str = Field(min_length=MIN_GAME_NAME_LEN, max_length=MAX_GAME_NAME_LEN)
    game_category: str = Field(min_length=MIN_CATEGORY_LEN, max_length=MAX_CATEGORY_LEN)

    @field_validator("game_category")
    @classmethod
    def check_category(cls, category: str) -> str:
        if category not in [game_cat.value for game_cat in GameCategory]:
            raise ValidationError(f"Invalid {category=}")
        return category


class GameRoomView(GameRoomSchema):
    id: int = valid_id
    model_config = ConfigDict(from_attributes=True)


class PlayerSchema(BaseModel):
    name: str = Field(min_length=MIN_PLAYER_NAME_LEN, max_length=MAX_PLAYER_NAME_LEN)


class PlayerView(PlayerSchema):
    id: int = valid_id
    games_played: int
    games_won: int
    score: float
    model_config = ConfigDict(from_attributes=True)


class PlayerWithGameView(PlayerView):
    game: Optional[GameRoomView]


class GameRoomWithPlayersView(GameRoomView):
    players: list[PlayerView]
