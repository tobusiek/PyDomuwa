from fastapi import status
from fastapi.testclient import TestClient

from domuwa.models import Player
from domuwa.services.players_services import PlayerServices
from tests.common_tc import CommonTestCase
from tests.factories import PlayerFactory


class TestPlayer(CommonTestCase[Player]):
    path = "/api/players/"
    services = PlayerServices()

    def assert_valid_response(self, response_data: dict) -> None:
        assert "id" in response_data, response_data
        assert "name" in response_data, response_data
        assert "games_played" in response_data, response_data
        assert "games_won" in response_data, response_data

    def assert_valid_response_values(
        self,
        response_data: dict,
        model: Player,
    ) -> None:
        assert response_data["id"] == model.id
        assert response_data["name"] == model.name
        assert response_data["games_played"] == model.games_played
        assert response_data["games_won"] == model.games_won

    def build_model(self) -> Player:
        return PlayerFactory.build()

    def create_model(self) -> Player:
        return PlayerFactory.create()

    def test_create_non_unique_name(self, api_client: TestClient):
        player = PlayerFactory.create()
        response = api_client.post(
            self.path,
            json={"name": player.name},
        )
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    def test_update(self, api_client: TestClient):
        player_old = PlayerFactory.create()
        player_new = PlayerFactory.build()

        response = api_client.patch(
            f"{self.path}{player_old.id}",
            json=player_new.model_dump(),
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)
        assert player_new.name == response_data["name"]

        response = api_client.get(f"{self.path}{player_old.id}")
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)
        assert player_new.name == response_data["name"]
