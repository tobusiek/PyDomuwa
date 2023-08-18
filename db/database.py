from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session

DATABASE_URL = "sqlite:///./database.db"
engine = create_engine(DATABASE_URL)

Base = declarative_base()
Base.metadata.create_all(bind=engine)


def get_db():
    db = Session(autocommit=True, autoflush=False, bind=engine)
    try:
        yield db
    finally:
        db.close()
