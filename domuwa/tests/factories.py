import factory

from domuwa import models


class QuestionFactory(factory.alchemy.SQLAlchemyModelFactory):
    game_name = "ego"
    category = "SFW"
    author = factory.Sequence(lambda x: "Author %d" % x)
    text = "question's text"
    excluded = False

    class Meta:
        model = models.Question


class AnswerFactory(factory.alchemy.SQLAlchemyModelFactory):
    author = factory.Sequence(lambda x: "Author %d" % x)
    text = "answer's text"
    correct = False
    question = factory.SubFactory(QuestionFactory)

    class Meta:
        model = models.Answer


class GameRoomFactory(factory.alchemy.SQLAlchemyModelFactory):
    game_name = "ego"
    game_category = "SFW"

    class Meta:
        model = models.GameRoom


class PlayerFactory(factory.alchemy.SQLAlchemyModelFactory):
    name = factory.Sequence(lambda x: "Player %d" % x)
    games_played = 0
    games_won = 0
    score = 0
    game_room = factory.SubFactory(GameRoomFactory)

    class Meta:
        model = models.Player
