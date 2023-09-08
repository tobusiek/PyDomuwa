from collections.abc import AsyncGenerator
from typing import Type, TypeVar

from fastapi import Depends, HTTPException, status
from sqlalchemy import StaticPool, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import Session, sessionmaker

import config

ORMModel = TypeVar("ORMModel")

engine = create_engine(
    config.DATABASE_URL,
    connect_args={"check_same_thread": False},
    poolclass=StaticPool
)
SessionLocal = sessionmaker(autoflush=True, bind=engine)

Base: ORMModel = declarative_base()


def init_db():
    Base.metadata.create_all(engine)


async def get_db() -> AsyncGenerator[Session, None]:
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


async def get_obj_of_type_by_id(
        obj_id: int,
        obj_model_type: ORMModel,
        obj_model_type_name: str,
        db: Session = Depends(get_db)
) -> ORMModel:
    obj = db.query(obj_model_type).get(obj_id)
    if not obj:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"{obj_model_type_name} of id={obj_id} not found")
    return obj


async def get_all_objs_of_type(obj_model: ORMModel, db: Session = Depends(get_db)) -> list[ORMModel]:
    return db.query(obj_model).all()


async def db_obj_save(obj_model: ORMModel | Type[ORMModel], db: Session = Depends(get_db)) -> ORMModel:
    db.add(obj_model)
    db.commit()
    db.refresh(obj_model)
    return obj_model


async def db_obj_delete(
        obj_id: int,
        obj_model_type: ORMModel,
        obj_model_type_name: str,
        db: Session = Depends(get_db)
) -> None:
    obj = await get_obj_of_type_by_id(obj_id, obj_model_type, obj_model_type_name, db)
    db.delete(obj)
    db.commit()
