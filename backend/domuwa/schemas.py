import enum
from typing import Optional

import pydantic

from domuwa.utils.logging import get_logger

logger = get_logger("validator")

MIN_ID = 1
MIN_PLAYER_NAME_LEN = 3
MAX_PLAYER_NAME_LEN = 25
MIN_TEXT_LEN = 1
MAX_TEXT_LEN = 150

valid_id = pydantic.Field(ge=1)


class AnswerSchema(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    author: str = pydantic.Field(
        min_length=MIN_PLAYER_NAME_LEN,
        max_length=MAX_PLAYER_NAME_LEN,
    )
    text: str = pydantic.Field(min_length=MIN_TEXT_LEN, max_length=MAX_TEXT_LEN)
    correct: bool = pydantic.Field(False)
    question_id: int = pydantic.Field(strict=True, ge=MIN_ID)


class AnswerView(AnswerSchema):
    id: int = valid_id


MIN_GAME_NAME_LEN = 3
MAX_GAME_NAME_LEN = 15
MIN_CATEGORY_LEN = 3
MAX_CATEGORY_LEN = 25


class GameCategory(enum.Enum):
    SFW = "SFW"
    NSFW = "NSFW"
    MIXED = "MIXED"


def check_category(category: str) -> str:
    if category not in [game_cat.value for game_cat in GameCategory]:
        raise ValueError(f"Invalid {category=}")
    return category


class QuestionSchema(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    game_name: str = pydantic.Field(
        min_length=MIN_GAME_NAME_LEN,
        max_length=MAX_GAME_NAME_LEN,
    )
    category: str = pydantic.Field(
        min_length=MIN_CATEGORY_LEN,
        max_length=MAX_CATEGORY_LEN,
    )
    author: str = pydantic.Field(
        min_length=MIN_PLAYER_NAME_LEN,
        max_length=MAX_PLAYER_NAME_LEN,
    )
    text: str = pydantic.Field(min_length=MIN_TEXT_LEN, max_length=MAX_TEXT_LEN)
    excluded: bool = pydantic.Field(False)

    @pydantic.field_validator("game_name", mode="before")
    @classmethod
    def check_game_name(cls, game_name: str) -> str:
        if game_name not in ("ego", "who's-most-likely"):
            logger.warning("Invalid data")
            raise ValueError(f"Invalid game name={game_name}")
        logger.info("valid data")
        return game_name

    @pydantic.field_validator("category", mode="before")
    @classmethod
    def check_category(cls, category: str) -> str:
        return check_category(category)


class QuestionView(QuestionSchema):
    id: int = valid_id


class QuestionWithAnswersView(QuestionView):
    answers: list[AnswerView]


class AnswerWithQuestionView(AnswerView):
    question: QuestionView


class GameRoomSchema(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    game_name: str = pydantic.Field(
        min_length=MIN_GAME_NAME_LEN,
        max_length=MAX_GAME_NAME_LEN,
    )
    game_category: str = pydantic.Field(
        min_length=MIN_CATEGORY_LEN,
        max_length=MAX_CATEGORY_LEN,
    )

    @pydantic.field_validator("game_category")
    @classmethod
    def check_category(cls, category: str) -> str:
        return check_category(category)


class GameRoomView(GameRoomSchema):
    id: int = valid_id


class PlayerSchema(pydantic.BaseModel):
    model_config = pydantic.ConfigDict(from_attributes=True)

    name: str = pydantic.Field(
        min_length=MIN_PLAYER_NAME_LEN,
        max_length=MAX_PLAYER_NAME_LEN,
    )


class PlayerView(PlayerSchema):
    id: int = valid_id
    games_played: int
    games_won: int
    score: float


class PlayerWithGameView(PlayerView):
    game: Optional[GameRoomView]


class GameRoomWithPlayersView(GameRoomView):
    players: list[PlayerView]
