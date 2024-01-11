import dataclasses
from typing import Any

ResponseType = dict[str, str | int | float | bool]

ID = "id"
GAME_NAME = "game_name"
CATEGORY = "category"
AUTHOR = "author"
TEXT = "text"
EXCLUDED = "excluded"
ANSWERS = "answers"
ANSWER_ID = "answer_id"
CORRECT = "correct"
QUESTION_ID = "question_id"
QUESTION = "question"


@dataclasses.dataclass
class QuestionValid:
    game_name: str = "ego"
    category: str = "MIXED"
    author: str = "User"
    text: str = "text"
    excluded: bool = False

    # noinspection PyAttributeOutsideInit
    def add_id(self, question_id: int) -> None:
        self.question_id = question_id


@dataclasses.dataclass
class QuestionInvalid:
    game_name: Any = "ego"
    category: Any = "MIXED"
    author: Any = "User"
    text: Any = "text"
    excluded: Any = False

    # noinspection PyAttributeOutsideInit
    def add_id(self, question_id: int) -> None:
        self.question_id = question_id


TEST_QUESTIONS_VALID: list[QuestionValid] = [
    QuestionValid(author="User1", text="text 1"),
    QuestionValid(category="NSFW", author="User2", text="text 2", excluded=True),
    QuestionValid(
        game_name="who's most likely",
        category="SFW",
        author="User1",
        text="text 3",
        excluded=True,
    ),
]

TEST_QUESTIONS_INVALID: dict[str, QuestionInvalid] = {
    GAME_NAME: QuestionInvalid(game_name="invalid game"),
    CATEGORY: QuestionInvalid(category="invalid category"),
    AUTHOR: QuestionInvalid(author=["invalid author", 1]),
    TEXT: QuestionInvalid(text=""),
    EXCLUDED: QuestionInvalid(excluded=5),
}


@dataclasses.dataclass
class AnswerValid:
    author: str = "User"
    text: str = "text"
    correct: bool = False

    # noinspection PyAttributeOutsideInit
    def add_answer_id(self, answer_id: int) -> None:
        self.answer_id = answer_id

    # noinspection PyAttributeOutsideInit
    def add_question_id(self, question_id: int) -> None:
        self.question_id = question_id


@dataclasses.dataclass
class AnswerInvalid:
    question_id: Any = 1
    author: Any = "User"
    text: Any = "text"
    correct: Any = False

    # noinspection PyAttributeOutsideInit
    def add_answer_id(self, answer_id: int) -> None:
        self.answer_id = answer_id


TEST_ANSWERS_VALID: list[AnswerValid] = [
    AnswerValid(author="User1", text="text 1"),
    AnswerValid(author="User1", text="text 2", correct=True),
    AnswerValid(author="User2", text="text 3", correct=True),
]

TEST_ANSWERS_INVALID: dict[str, AnswerInvalid] = {
    AUTHOR: AnswerInvalid(author=None),
    TEXT: AnswerInvalid(text=None),
    CORRECT: AnswerInvalid(correct="null"),
    QUESTION_ID: AnswerInvalid(question_id=100),
}


@dataclasses.dataclass
class GameRoomValid:
    game_name: str = "ego"
    game_category: str = "MIXED"


@dataclasses.dataclass
class GameRoomInvalid:
    game_name: Any = "ego"
    game_category: Any = "MIXED"


@dataclasses.dataclass
class PlayerValid:
    name: str = "User"
    score: float = 0.0


@dataclasses.dataclass
class PlayerInvalid:
    name: Any = "User"
    score: Any = 0.0


TEST_GAME_ROOMS_VALID = []

TEST_PLAYERS_VALID = []

TEST_RANKINGS_VALID = []
