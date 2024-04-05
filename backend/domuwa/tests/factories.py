import factory
from factory.alchemy import SQLAlchemyModelFactory

from domuwa.models import db_models


class GameTypeFactory(SQLAlchemyModelFactory):
    name = db_models.GameTypeChoices.EGO

    class Meta:  # type: ignore
        model = db_models.GameType
        sqlalchemy_session_persistence = "commit"


class PlayerFactory(SQLAlchemyModelFactory):
    name = factory.Sequence(lambda x: "Player %d" % x)

    class Meta:  # type: ignore
        model = db_models.Player
        sqlalchemy_session_persistence = "commit"
