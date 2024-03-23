from collections.abc import AsyncGenerator
from typing import TypeVar

import fastapi
import sqlalchemy
from fastapi import status
from sqlalchemy import orm

from config import settings
from domuwa.utils import logging

logger = logging.get_logger("db_connector")

engine = sqlalchemy.create_engine(
    settings.DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=sqlalchemy.StaticPool,
)
SessionLocal = orm.sessionmaker(autoflush=True, bind=engine)

T = TypeVar("T")


async def get_db_session() -> AsyncGenerator[orm.Session, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_obj_of_type_by_id(
    obj_id: int,
    obj_model_type: type[T],
    obj_model_type_name: str,
    db: orm.Session = fastapi.Depends(get_db_session),
) -> T:
    obj = db.get(obj_model_type, obj_id)
    if not obj:
        logger.warning(f"{obj_model_type_name} of id={obj_id} not found")
        raise fastapi.HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"{obj_model_type_name} of id={obj_id} not found",
        )
    return obj


def get_all_objs_of_type(
    obj_model: type[T],
    db: orm.Session = fastapi.Depends(get_db_session),
) -> list[T]:
    return db.query(obj_model).all()


def save_obj(
    obj_model: T,
    db: orm.Session = fastapi.Depends(get_db_session),
) -> T:
    db.add(obj_model)
    db.commit()
    db.refresh(obj_model)
    return obj_model


def delete_obj(
    obj_id: int,
    obj_model_type: type[T],  # type: ignore
    obj_model_type_name: str,
    db: orm.Session = fastapi.Depends(get_db_session),
) -> None:
    obj = get_obj_of_type_by_id(obj_id, obj_model_type, obj_model_type_name, db)
    db.delete(obj)
    db.commit()
    logger.debug(f"{obj_model_type_name} of id={obj_id} deleted")
