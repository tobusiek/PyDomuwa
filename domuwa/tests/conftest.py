from collections.abc import Generator

import pytest
from fastapi.testclient import TestClient
from pytest_factoryboy import register
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, scoped_session, sessionmaker

from domuwa import config
from domuwa import database as db
from domuwa.models import Base
from domuwa.tests import factories
from main import app

config.TESTING = True

# SQLALCHEMY_DATABASE_URL = "sqlite:///test_database.db"
SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = scoped_session(sessionmaker(autoflush=False, bind=engine))


@pytest.fixture()
def db_session() -> Generator[Session, None, None]:
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # connection = engine.connect()
    # transaction = connection.begin()
    # db_sess = TestingSessionLocal(bind=connection)
    # yield db_sess
    #
    # db_sess.close()
    # transaction.rollback()
    # connection.close()

    with TestingSessionLocal() as db_sess:
        yield db_sess


@pytest.fixture()
def api_client(db_session: Session) -> Generator[TestClient, None, None]:
    def override_get_db_session() -> Generator[Session, None, None]:
        with db_session:
            yield db_session

    app.dependency_overrides[db.get_db_session] = override_get_db_session

    with TestClient(app) as client:
        yield client

    del app.dependency_overrides[db.get_db_session]


register(factories.AnswerFactory)
register(factories.QuestionFactory)
register(factories.GameRoomFactory)
register(factories.PlayerFactory)
