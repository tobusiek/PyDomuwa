from pytest_factoryboy import register

from domuwa.tests import factories

register(factories.AnswerFactory)
register(factories.QuestionFactory)
register(factories.GameRoomFactory)
register(factories.PlayerFactory)
