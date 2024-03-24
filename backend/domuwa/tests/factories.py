import factory
from factory.alchemy import SQLAlchemyModelFactory

from domuwa import models
from domuwa.sqlmodels.player import Player


class QuestionFactory(SQLAlchemyModelFactory):
    game_name = "ego"
    category = "SFW"
    author = factory.Sequence(lambda x: "Author %d" % x)
    text = "question's text"
    excluded = False

    class Meta:  # type: ignore
        model = models.Question


class AnswerFactory(SQLAlchemyModelFactory):
    author = factory.Sequence(lambda x: "Author %d" % x)
    text = "answer's text"
    correct = False
    question: factory.SubFactory = factory.SubFactory(QuestionFactory)

    class Meta:  # type: ignore
        model = models.Answer


class GameRoomFactory(SQLAlchemyModelFactory):
    game_name = "ego"
    game_category = "SFW"

    class Meta:  # type: ignore
        model = models.GameRoom


class PlayerFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda x: "Player %d" % x)

    class Meta:  # type: ignore
        model = Player
        sqlalchemy_session_persistence = "commit"
