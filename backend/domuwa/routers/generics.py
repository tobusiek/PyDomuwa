import logging
from abc import ABC
from typing import Generic

from fastapi import HTTPException, status
from sqlmodel import Session

from domuwa.services.common_services import (
    CommonServices,
    CreateModelT,
    DbModelT,
    UpdateModelT,
)


class GenericRouter(ABC, Generic[CreateModelT, UpdateModelT, DbModelT]):
    services: CommonServices[CreateModelT, UpdateModelT, DbModelT]
    logger: logging.Logger
    db_model_type_name: str

    async def _get_instance(self, model_id: int, session: Session):
        instance = await self.services.get_by_id(model_id, session)
        if instance is None:
            err_msg = f"{self.db_model_type_name}(id={model_id}) not found"
            self.logger.error(err_msg)
            raise HTTPException(status.HTTP_404_NOT_FOUND, err_msg)
        return instance


class RetrieveRouter(GenericRouter, Generic[DbModelT]):
    async def _get_by_id(self, model_id: int, session: Session):
        return await self._get_instance(model_id, session)

    async def _get_all(self, session: Session):
        return await self.services.get_all(session)


class CreateRouter(GenericRouter, Generic[CreateModelT, DbModelT]):
    async def _post(self, create_model: CreateModelT, session: Session):
        self.logger.debug(
            "got %s(%s) to create",
            self.db_model_type_name,
            create_model,
        )
        return await self.services.create(create_model, session)


class UpdateRouter(GenericRouter, Generic[UpdateModelT, DbModelT]):
    async def _patch(
        self,
        model_id: int,
        model_update: UpdateModelT,
        session: Session,
    ):
        self.logger.debug(
            "got %s(%s) to update %s(id=%d)",
            self.db_model_type_name,
            model_update,
            self.db_model_type_name,
            model_id,  # type: ignore
        )
        model = await self._get_instance(model_id, session)
        return self.services.update(model, model_update, session)


class DeleteRouter(GenericRouter, Generic[DbModelT]):
    async def _delete(self, model_id: int, session: Session):
        self.logger.debug(
            "got %s(id=%d) to delete",
            self.db_model_type_name,
            model_id,  # type: ignore
        )
        model = await self._get_instance(model_id, session)
        return await self.services.delete(model, session)
