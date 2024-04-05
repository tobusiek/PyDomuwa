from typing import Any

from fastapi.testclient import TestClient
from starlette import status

from domuwa.tests.factories import PlayerFactory

PLAYERS_PREFIX = "/api/players/"


def assert_valid_response(response: dict[str, Any]):
    assert "id" in response, response
    assert "name" in response, response
    assert "games_played" in response, response
    assert "games_won" in response, response


def test_create_player(api_client: TestClient):
    player = {"name": "Player 1"}

    response = api_client.post(
        PLAYERS_PREFIX,
        json=player,
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    assert_valid_response(response_data)
    assert player["name"] == response_data["name"], response.text

    response = api_client.get(f'{PLAYERS_PREFIX}{response_data["id"]}')
    assert response.status_code == status.HTTP_200_OK, response.text
    assert_valid_response(response.json())


def test_create_player_invalid_name(api_client: TestClient):
    response = api_client.post(
        PLAYERS_PREFIX,
        json={"name": "x"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


def test_create_player_non_unique_name(api_client: TestClient):
    player = PlayerFactory.create()
    response = api_client.post(
        PLAYERS_PREFIX,
        json={"name": player.name},
    )
    assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text


def test_get_player_by_id(api_client: TestClient):
    player = PlayerFactory.create()
    response = api_client.get(f"{PLAYERS_PREFIX}{player.id}")
    assert response.status_code == status.HTTP_200_OK, response.text


def test_get_non_existing_player(api_client: TestClient):
    response = api_client.get(f"{PLAYERS_PREFIX}999")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_all_players(api_client: TestClient, count: int = 3):
    PlayerFactory.create_batch(count)

    response = api_client.get(PLAYERS_PREFIX)
    assert response.status_code == status.HTTP_200_OK
    response_data = response.json()

    assert isinstance(response_data, list), response.text
    assert len(response_data) >= count, response.text

    for player in response_data:
        assert_valid_response(player)


def test_update_player(api_client: TestClient):
    player_old = PlayerFactory.create()
    player_new = PlayerFactory.build()

    response = api_client.patch(
        f"{PLAYERS_PREFIX}{player_old.id}",
        json=player_new.model_dump(),
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert_valid_response(response_data)
    assert player_new.name == response_data["name"]

    response = api_client.get(f"{PLAYERS_PREFIX}{player_old.id}")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert_valid_response(response_data)
    assert player_new.name == response_data["name"]


def test_update_non_existing_player(api_client: TestClient):
    response = api_client.patch(
        f"{PLAYERS_PREFIX}{999}",
        json={"name": "Player 1"},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_update_player_invalid_name(api_client: TestClient):
    player = PlayerFactory.create()
    response = api_client.patch(
        f"{PLAYERS_PREFIX}{player.id}",
        json={"name": "x"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


def test_delete_player(api_client: TestClient):
    player = PlayerFactory.create()
    response = api_client.delete(f"{PLAYERS_PREFIX}{player.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    response = api_client.get(f"{PLAYERS_PREFIX}{player.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_delete_non_existing_player(api_client: TestClient):
    response = api_client.delete(f"{PLAYERS_PREFIX}{999}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
