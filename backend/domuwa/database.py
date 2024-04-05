import logging
from typing import TypeVar

from fastapi import Depends, HTTPException, status
from sqlmodel import SQLModel, Session, create_engine, select

from domuwa.config import settings

logger = logging.getLogger(__name__)

engine = create_engine(settings.DATABASE_URL, connect_args={"check_same_thread": False})


ModelType = TypeVar("ModelType", bound=SQLModel)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)


def get_db_session():
    with Session(engine) as db_sess:
        yield db_sess


async def get(
    model_id: int,
    model_type: type[ModelType],
    db_sess: Session = Depends(get_db_session),
):
    obj = db_sess.get(model_type, model_id)
    if not obj:
        err_msg = f"{model_type.__name__}(id={model_id}) not found"
        logger.warning(err_msg)
        raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)

    logger.debug(f"got {model_type.__name__}({obj}) from db")
    return obj


async def get_all(
    model_type: type[ModelType],
    db_sess: Session = Depends(get_db_session),
):
    logger.debug(f"getting all {model_type.__name__} from db")
    return db_sess.exec(select(model_type)).all()


async def save(
    model: ModelType,  # type: ignore
    db: Session = Depends(get_db_session),
):
    db.add(model)
    db.commit()
    db.refresh(model)
    logger.debug(f"saved {model.__class__.__name__}({model}) to db")
    return model


async def update(
    model_id: int,
    model: ModelType,  # type: ignore
    db_sess: Session = Depends(get_db_session),
):
    db_obj = await get(model_id, type(model), db_sess)
    obj_data = model.model_dump(exclude_unset=True)
    db_obj.sqlmodel_update(obj_data)
    db_sess.add(db_obj)
    db_sess.commit()
    db_sess.refresh(db_obj)
    logger.debug(
        f"updated {model.__class__.__name__}({model}) to {model.__class__.__name__}({db_obj})"
    )
    return db_obj


async def delete(
    model_id: int,
    model_type: type[ModelType],
    db: Session = Depends(get_db_session),
):
    obj = await get(model_id, model_type, db)
    db.delete(obj)
    db.commit()
    logger.debug(f"{model_type.__name__}(id={model_id}) deleted")
