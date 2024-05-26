import factory
from factory.alchemy import SQLAlchemyModelFactory

from domuwa.models.answer import Answer
from domuwa.models.game_type import GameType, GameTypeChoices
from domuwa.models.player import Player
from domuwa.models.qna_category import QnACategory, QnACategoryChoices
from domuwa.models.question import Question


class GameTypeFactory(SQLAlchemyModelFactory):
    name = GameTypeChoices.EGO

    class Meta:  # type: ignore
        model = GameType
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_get_or_create = ("name",)


class PlayerFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda x: "Player %d" % x)

    class Meta:  # type: ignore
        model = Player
        sqlalchemy_session_persistence = "commit"


class QnACategoryFactory(SQLAlchemyModelFactory):
    name = QnACategoryChoices.SFW

    class Meta:  # type: ignore
        model = QnACategory
        sqlalchemy_session_persistence = "commit"
        sqlalchemy_get_or_create = ("name",)


class AnswerFactory(SQLAlchemyModelFactory):
    text: str = "answer text"
    excluded: bool = False
    author_id: int
    game_type_id: int
    game_category_id: int
    question_id: int | None = None

    class Meta:  # type: ignore
        model = Answer
        sqlalchemy_session_persistence = "commit"


class QuestionFactory(SQLAlchemyModelFactory):
    text: str = "question text"
    excluded: bool = False
    author_id: int
    game_type_id: int
    game_category_id: int

    class Meta:  # type: ignore
        model = Question
        sqlalchemy_session_persistence = "commit"
