from typing import TypeVar

from config import settings
from fastapi import Depends, HTTPException, status
from sqlmodel import SQLModel, Session, create_engine, select

from domuwa import logging

logger = logging.get_logger("db_connector")

engine = create_engine(
    settings.DATABASE_URL,
    echo=True,
    connect_args={"check_same_thread": False},
)


class SQLModelWithId(SQLModel):
    id: int


ModelType = TypeVar("ModelType", bound=SQLModel)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db_session():
    with Session(engine) as db_sess:
        yield db_sess


def get_obj_of_type_by_id(
    obj_id: int,
    obj_model_type: type[ModelType],
    obj_model_type_name: str,
    db_sess: Session = Depends(get_db_session),
):
    obj = db_sess.get(obj_model_type, obj_id)
    if not obj:
        logger.warning(f"{obj_model_type_name} of id={obj_id} not found")
        raise HTTPException(
            status.HTTP_404_NOT_FOUND,
            f"{obj_model_type_name} of id={obj_id} not found",
        )
    return obj


def get_all_objs_of_type(
    obj_model: type[ModelType],
    db_sess: Session = Depends(get_db_session),
):
    return db_sess.exec(select(obj_model)).all()


def save_obj(
    obj_model: ModelType,  # type: ignore
    db: Session = Depends(get_db_session),
):
    db.add(obj_model)
    db.commit()
    db.refresh(obj_model)
    return obj_model


def update_obj(
    obj_id: int,
    obj_model: ModelType,  # type: ignore
    ojb_model_type_name: str,
    db_sess: Session = Depends(get_db_session),
):
    db_obj = get_obj_of_type_by_id(
        obj_id, type(obj_model), ojb_model_type_name, db_sess
    )
    obj_data = obj_model.model_dump(exclude_unset=True)
    db_obj.sqlmodel_update(obj_data)
    db_sess.add(db_obj)
    db_sess.commit()
    db_sess.refresh(db_obj)
    return db_obj


def delete_obj(
    obj_id: int,
    obj_model_type: type[ModelType],
    obj_model_type_name: str,
    db: Session = Depends(get_db_session),
):
    obj = get_obj_of_type_by_id(obj_id, obj_model_type, obj_model_type_name, db)
    db.delete(obj)
    db.commit()
    logger.debug(f"{obj_model_type_name} of id={obj_id} deleted")
