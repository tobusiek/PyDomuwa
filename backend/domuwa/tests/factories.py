import factory
from factory import Factory

from domuwa import models


class QuestionFactory(Factory):
    game_name = "ego"
    category = "SFW"
    author = factory.Sequence(lambda x: "Author %d" % x)
    text = "question's text"
    excluded = False

    class Meta:  # type: ignore
        model = models.Question


class AnswerFactory(Factory):
    author = factory.Sequence(lambda x: "Author %d" % x)
    text = "answer's text"
    correct = False
    question: factory.SubFactory = factory.SubFactory(QuestionFactory)

    class Meta:  # type: ignore
        model = models.Answer


class GameRoomFactory(Factory):
    game_name = "ego"
    game_category = "SFW"

    class Meta:  # type: ignore
        model = models.GameRoom


class PlayerFactory(Factory):
    name = factory.Sequence(lambda x: "Player %d" % x)

    class Meta:  # type: ignore
        model = models.Player
