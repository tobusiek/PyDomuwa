from abc import ABC, abstractmethod
from typing import Generic, TypeVar

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import SQLModel, Session

from domuwa.services.common_services import CommonServices

DbModelT = TypeVar('DbModelT', bound=SQLModel)


class CommonTestCase(ABC, Generic[DbModelT]):
    path: str
    services: CommonServices

    @abstractmethod
    def assert_valid_response(self, response_data: dict) -> None:
        pass

    @abstractmethod
    def assert_valid_response_values(
        self, response_data: dict, model: DbModelT,
    ) -> None:
        pass

    async def assert_valid_delete(self, model_id: int, db_session: Session) -> None:
        assert await self.services.get_by_id(model_id, db_session) is None

    @abstractmethod
    def build_model(self) -> DbModelT:
        pass

    @abstractmethod
    def create_model(self) -> DbModelT:
        pass

    @pytest.mark.asyncio
    async def test_create(self, api_client: TestClient, db_session: Session):
        model = self.build_model()

        response = api_client.post(self.path, json=model.model_dump())
        assert response.status_code == status.HTTP_201_CREATED, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)

        response = api_client.get(f"{self.path}{response_data['id']}")
        assert response.status_code == status.HTTP_200_OK, response.text
        self.assert_valid_response(response.json())

        assert await self.services.get_by_id(response_data['id'], db_session) is not None

    def test_get_by_id(self, api_client: TestClient):
        model = self.create_model()

        response = api_client.get(f"{self.path}{model.id}")  # type: ignore
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)
        self.assert_valid_response_values(response_data, model)

    def test_get_all(self, api_client: TestClient, model_count: int = 3):
        for _ in range(model_count):
            self.create_model()

        response = api_client.get(self.path)
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()

        assert isinstance(response_data, list), response_data
        assert len(response_data) == model_count, response_data
        for model_data in response_data:
            self.assert_valid_response(model_data)

    @abstractmethod
    def test_update(self, api_client: TestClient):
        pass

    @pytest.mark.asyncio
    async def test_delete(self, api_client: TestClient, db_session: Session):
        model = self.create_model()
        model_id = model.id  # type: ignore

        response = api_client.delete(f"{self.path}{model_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

        response = api_client.get(f"{self.path}{model_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

        await self.assert_valid_delete(model_id, db_session)
