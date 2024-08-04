from fastapi import status
from fastapi.testclient import TestClient

from domuwa.models.game_type import GameType, GameTypeChoices
from domuwa.services.game_type_services import GameTypeServices
from tests.common_tc import CommonTestCase
from tests.factories import GameTypeFactory


class TestGameType(CommonTestCase[GameType]):
    path = "/api/game-types/"
    services = GameTypeServices()

    def assert_valid_response(self, response_data: dict) -> None:
        assert "id" in response_data, response_data
        assert "name" in response_data, response_data
        assert (
                response_data["name"] in GameTypeChoices._value2member_map_
        ), response_data

    def assert_valid_response_values(
        self,
        response_data: dict,
        model: GameType,
    ) -> None:
        assert response_data["id"] == model.id
        assert response_data["name"] == model.name

    def build_model(self) -> GameType:
        return GameTypeFactory.build()

    def create_model(self) -> GameType:
        return GameTypeFactory.create()

    def test_create_invalid_name(self, api_client: TestClient):
        response = api_client.post(self.path, json={"name": "not from enum"})
        assert (
                response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text

    def test_get_all(self, api_client: TestClient, model_count: int = 3):
        GameTypeFactory.create(name=GameTypeChoices.EGO)
        GameTypeFactory.create(name=GameTypeChoices.WHOS_MOST_LIKELY)
        GameTypeFactory.create(name=GameTypeChoices.GENTLEMENS_CARDS)

        response = api_client.get(self.path)
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()

        assert isinstance(response_data, list), response_data
        assert len(response_data) >= 3, response_data

        for game_type in response_data:
            self.assert_valid_response(game_type)

    def test_update(self, api_client: TestClient):
        game_type = GameTypeFactory.create(name=GameTypeChoices.EGO)
        updated_game_type_data = {"name": GameTypeChoices.WHOS_MOST_LIKELY}

        response = api_client.patch(
            f"{self.path}{game_type.id}",
            json=updated_game_type_data,
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        self.assert_valid_response(response.json())

        response = api_client.get(f"{self.path}{game_type.id}")
        assert response.status_code == status.HTTP_200_OK, response.text

        response_data = response.json()
        self.assert_valid_response(response_data)
        assert response_data["name"] == updated_game_type_data["name"], response_data

    def test_update_invalid_name(self, api_client: TestClient):
        game_type = GameTypeFactory.create()

        response = api_client.patch(
            f"{self.path}{game_type.id}",
            json={"name": "not from enum"},
        )
        assert (
                response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
        ), response.text
