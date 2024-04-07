import factory
from factory.alchemy import SQLAlchemyModelFactory

from domuwa.models.game_type import GameType, GameTypeChoices
from domuwa.models.player import Player


class GameTypeFactory(SQLAlchemyModelFactory):
    name = GameTypeChoices.EGO

    class Meta:  # type: ignore
        model = GameType
        sqlalchemy_session_persistence = "commit"


class PlayerFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda x: "Player %d" % x)

    class Meta:  # type: ignore
        model = Player
        sqlalchemy_session_persistence = "commit"
