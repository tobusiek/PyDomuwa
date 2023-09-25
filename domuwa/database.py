from collections.abc import AsyncGenerator
from logging import getLogger
from typing import Type, TypeVar

from fastapi import Depends, HTTPException, status
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.orm import Session, declarative_base, sessionmaker

from domuwa import config

logger = getLogger("db_connector")

ORM = TypeVar("ORM")

engine = create_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base: ORM = declarative_base()


async def get_db() -> AsyncGenerator[Session, None]:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


async def get_obj_of_type_by_id(
        obj_id: int,
        obj_model_type: ORM,
        obj_model_type_name: str,
        db: Session = Depends(get_db),
) -> ORM:
    obj = db.get(obj_model_type, obj_id)
    if not obj:
        logger.warning(f"{obj_model_type_name} of id={obj_id} not found")
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{obj_model_type_name} of id={obj_id} not found")
    return obj


async def get_all_objs_of_type(obj_model: ORM, db: Session = Depends(get_db)) -> list[ORM]:
    return db.query(obj_model).all()


async def db_obj_save(obj_model: ORM | Type[ORM], db: Session = Depends(get_db)) -> ORM:
    db.add(obj_model)
    db.commit()
    db.refresh(obj_model)
    return obj_model


async def db_obj_delete(
        obj_id: int,
        obj_model_type: ORM,
        obj_model_type_name: str,
        db: Session = Depends(get_db),
) -> None:
    obj = await get_obj_of_type_by_id(obj_id, obj_model_type, obj_model_type_name, db)
    db.delete(obj)
    db.commit()
    logger.debug(f"{obj_model_type_name} of id={obj_id} deleted")
