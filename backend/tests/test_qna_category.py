from fastapi import status
from fastapi.testclient import TestClient

from domuwa.models.qna_category import QnACategory, QnACategoryChoices
from domuwa.services.qna_categories_services import QnACategoryServices
from tests.common_tc import CommonTestCase
from tests.factories import QnACategoryFactory


class TestQnACategory(CommonTestCase[QnACategory]):
    path = "/api/qna-categories/"
    services = QnACategoryServices()

    def assert_valid_response(self, response_data: dict) -> None:
        assert "id" in response_data, response_data
        assert "name" in response_data, response_data
        assert (
            response_data["name"] in QnACategoryChoices._value2member_map_
        ), response_data

    def assert_valid_response_values(
        self, response_data: dict, model: QnACategory
    ) -> None:
        assert response_data["id"] == model.id
        assert response_data["name"] == model.name

    def build_model(self) -> QnACategory:
        return QnACategoryFactory.build()

    def create_model(self) -> QnACategory:
        return QnACategoryFactory.create()

    def test_update(self, api_client: TestClient):
        qna_category = QnACategoryFactory.create()
        updated_qna_category_data = {"name": QnACategoryChoices.NSFW}

        response = api_client.patch(
            f"{self.path}{qna_category.id}",
            json=updated_qna_category_data,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        self.assert_valid_response(response.json())

        response = api_client.get(f"{self.path}{qna_category.id}")
        assert response.status_code == status.HTTP_200_OK, response.text

        response_data = response.json()
        self.assert_valid_response(response_data)
        assert response_data["name"] == updated_qna_category_data["name"], response_data

    def test_create_invalid_name(self, api_client: TestClient):
        response = api_client.post(self.path, json={"name": "not from enum"})
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text

    def test_create_non_unique_name(self, api_client: TestClient):
        qna_category = QnACategoryFactory.create(name=QnACategoryChoices.SFW)

        response = api_client.post(self.path, json={"name": qna_category.name})
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    def test_update_invalid_name(self, api_client: TestClient):
        qna_category = QnACategoryFactory.create()

        response = api_client.patch(
            f"{self.path}{qna_category.id}",
            json={"name": "not from enum"},
        )
        assert (
            response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text

    def test_update_non_unique_name(self, api_client: TestClient):
        qna_category1 = QnACategoryFactory.create(name=QnACategoryChoices.SFW)
        qna_category2 = QnACategoryFactory.create(name=QnACategoryChoices.NSFW)

        response = api_client.patch(
            f"{self.path}{qna_category1.id}", json={"name": qna_category2.name}
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    def test_get_all(self, api_client: TestClient, model_count: int = 2):
        QnACategoryFactory.create(name=QnACategoryChoices.SFW)
        QnACategoryFactory.create(name=QnACategoryChoices.NSFW)

        response = api_client.get(self.path)
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()

        assert isinstance(response_data, list), response_data
        assert len(response_data) >= 2, response_data

        for qna_category in response_data:
            self.assert_valid_response(qna_category)
