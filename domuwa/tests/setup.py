from collections.abc import Generator

import sqlalchemy
from sqlalchemy import orm
from starlette import testclient

import main
from domuwa import config, models
from domuwa import database as db

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = sqlalchemy.create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=sqlalchemy.StaticPool,
)
TestingSessionLocal = orm.sessionmaker(autoflush=False, bind=engine)
models.Base.metadata.create_all(engine)


def override_get_db() -> Generator[orm.Session, None, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


main.app.dependency_overrides[db.get_db_session] = override_get_db

config.TESTING = True

client = testclient.TestClient(main.app)
