import factory
from factory.alchemy import SQLAlchemyModelFactory

from domuwa.models import db_models


class QuestionFactory(SQLAlchemyModelFactory):
    game_name = "ego"
    category = "SFW"
    author = factory.Sequence(lambda x: "Author %d" % x)
    text = "question's text"
    excluded = False

    class Meta:  # type: ignore
        model = db_models.Question


class AnswerFactory(SQLAlchemyModelFactory):
    author = factory.Sequence(lambda x: "Author %d" % x)
    text = "answer's text"
    correct = False
    question: factory.SubFactory = factory.SubFactory(QuestionFactory)

    class Meta:  # type: ignore
        model = db_models.Answer


class GameRoomFactory(SQLAlchemyModelFactory):
    game_name = "ego"
    game_category = "SFW"

    class Meta:  # type: ignore
        model = db_models.GameRoom


class PlayerFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda x: "Player %d" % x)

    class Meta:  # type: ignore
        model = db_models.Player
        sqlalchemy_session_persistence = "commit"
