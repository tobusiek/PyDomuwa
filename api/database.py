from collections.abc import AsyncGenerator

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session

import config

engine = create_engine(config.DATABASE_URL)
SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base = declarative_base()

TABLES_INITIALIZED = False


async def get_db() -> AsyncGenerator[Session, None]:
    global TABLES_INITIALIZED

    if not TABLES_INITIALIZED:
        Base.metadata.create_all(engine)
        TABLES_INITIALIZED = True

    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
