import logging
from abc import ABC, abstractmethod
from typing import Generic, final

from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import SQLModel, Session
from starlette.responses import Response

from domuwa.database import get_db_session
from domuwa.services.common_services import (
    CommonServices,
    CreateModelT,
    DbModelT,
    UpdateModelT,
)


class CommonRouter(ABC, Generic[CreateModelT, UpdateModelT, DbModelT]):
    prefix: str
    tags: list[str]
    router: APIRouter
    response_model: type[SQLModel]
    services: CommonServices[CreateModelT, UpdateModelT, DbModelT]
    logger: logging.Logger
    db_model_type_name: str
    __lookup = "{model_id}"

    def __init__(self) -> None:
        super().__init__()

        self.router.add_api_route(
            "/",
            self.create,
            status_code=status.HTTP_201_CREATED,
            methods=["POST"],
            response_model=self.response_model,
        )
        self.router.add_api_route(
            "/",
            self.get_all,
            methods=["GET"],
            response_model=list[self.response_model],  # type: ignore
        )
        self.router.add_api_route(
            f"/{self.__lookup}",
            self.get_by_id,
            methods=["GET"],
            response_model=self.response_model,
        )
        self.router.add_api_route(
            f"/{self.__lookup}",
            self.update,
            response_model=self.response_model,
            methods=["PATCH"],
        )
        self.router.add_api_route(
            f"/{self.__lookup}",
            self.delete,
            status_code=status.HTTP_204_NO_CONTENT,
            methods=["DELETE"],
            response_class=Response,
        )

    @final
    async def get_instance(
        self,
        model_id: int,
        session: Session = Depends(get_db_session),
    ) -> DbModelT:
        instance = await self.services.get_by_id(model_id, session)
        if instance is None:
            err_msg = f"{self.db_model_type_name}(id={model_id}) not found"
            self.logger.error(err_msg)
            raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)
        return instance

    async def get_by_id(
        self,
        model_id: int,
        session: Session = Depends(get_db_session),
    ):
        return await self.get_instance(model_id, session)

    async def get_all(self, session: Session = Depends(get_db_session)):
        return await self.services.get_all(session)

    @abstractmethod
    async def create(
        self,
        model: CreateModelT,
        session: Session = Depends(get_db_session),
    ):
        self.logger.debug(
            "got %s(%s) to create",
            self.db_model_type_name,
            model,
        )
        return await self.services.create(model, session)

    @abstractmethod
    async def update(
        self,
        model_id: int,
        model_update: UpdateModelT,
        session: Session = Depends(get_db_session),
    ):
        self.logger.debug(
            "got %s(%s) to update %s(id=%d)",
            self.db_model_type_name,
            model_update,
            self.db_model_type_name,
            model_id,  # type: ignore
        )
        model = await self.get_instance(model_id, session)
        return await self.services.update(model, model_update, session)

    async def delete(self, model_id: int, session: Session = Depends(get_db_session)):
        self.logger.debug(
            "got %s(id=%d) to delete",
            self.db_model_type_name,
            model_id,  # type: ignore
        )
        model = await self.get_instance(model_id, session)
        return await self.services.delete(model, session)


class CommonRouter400OnSaveError(CommonRouter[CreateModelT, UpdateModelT, DbModelT]):
    @abstractmethod
    async def create(
        self,
        model: CreateModelT,
        session: Session = Depends(get_db_session),
    ):
        db_model = await super().create(model, session)
        if db_model is None:
            err_msg = f"{self.db_model_type_name}({model}) cannot be created"
            self.logger.warning(err_msg)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, err_msg)
        return db_model

    @abstractmethod
    async def update(
        self,
        model_id: int,
        model_update: UpdateModelT,
        session: Session = Depends(get_db_session),
    ):
        db_model = await self.get_instance(model_id, session)
        model_updated = await self.services.update(db_model, model_update, session)
        if model_updated is None:
            err_msg = f"{self.db_model_type_name}(id={model_id}) cannot be updated with {self.db_model_type_name}({model_update})"
            self.logger.warning(err_msg)
            raise HTTPException(status.HTTP_400_BAD_REQUEST, err_msg)
        return model_updated
