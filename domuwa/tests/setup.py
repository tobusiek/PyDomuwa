from collections.abc import Generator

from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, sessionmaker
from starlette.testclient import TestClient

from domuwa import config
from domuwa.database import Base, get_db
from main import app

SQLALCHEMY_DATABASE_URL = "sqlite://"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(autoflush=False, bind=engine)

Base.metadata.create_all(bind=engine)


def override_get_db() -> Generator[Session, None]:
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db

config.TESTING = True
client = TestClient(app)
