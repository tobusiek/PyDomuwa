from typing import Any

from fastapi import status
from fastapi.testclient import TestClient

from domuwa.models.game_type import GameTypeChoices
from domuwa.tests.factories import GameTypeFactory

GAME_TYPES_PREFIX = "/api/game-types/"


def assert_valid_response(response_data: dict[str, Any]):
    assert "id" in response_data, response_data
    assert "name" in response_data, response_data
    assert response_data["name"] in GameTypeChoices._value2member_map_, response_data


def test_create_game_type(api_client: TestClient):
    response = api_client.post(
        GAME_TYPES_PREFIX,
        json={"name": GameTypeChoices.EGO},
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    assert_valid_response(response_data)

    response = api_client.get(f'{GAME_TYPES_PREFIX}{response_data["id"]}')
    assert response.status_code == status.HTTP_200_OK, response.text
    assert_valid_response(response.json())


def test_create_game_type_invalid_name(api_client: TestClient):
    response = api_client.post(
        GAME_TYPES_PREFIX,
        json={"name": "not from enum"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


def test_get_game_type_by_id(api_client: TestClient):
    game_type = GameTypeFactory.create()
    response = api_client.get(f"{GAME_TYPES_PREFIX}{game_type.id}")
    assert response.status_code == status.HTTP_200_OK, response.text
    assert_valid_response(response.json())


def test_get_non_existing_game_type(api_client: TestClient):
    response = api_client.get(f"{GAME_TYPES_PREFIX}999")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_get_all_game_types(api_client: TestClient):
    GameTypeFactory.create(name=GameTypeChoices.EGO)
    GameTypeFactory.create(name=GameTypeChoices.WHOS_MOST_LIKELY)
    GameTypeFactory.create(name=GameTypeChoices.GENTLEMENS_CARDS)

    response = api_client.get(GAME_TYPES_PREFIX)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()

    assert isinstance(response_data, list), response_data
    assert len(response_data) >= 3, response_data

    for game_type in response_data:
        assert_valid_response(game_type)


def test_update_game_type(api_client: TestClient):
    game_type = GameTypeFactory.create()
    updated_game_type_data = {"name": GameTypeChoices.WHOS_MOST_LIKELY}

    response = api_client.patch(
        f"{GAME_TYPES_PREFIX}{game_type.id}",
        json=updated_game_type_data,
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    assert_valid_response(response.json())

    response = api_client.get(f"{GAME_TYPES_PREFIX}{game_type.id}")
    assert response.status_code == status.HTTP_200_OK, response.text

    response_data = response.json()
    assert_valid_response(response_data)
    assert response_data["name"] == updated_game_type_data["name"], response_data


def test_update_non_existing_game_type(api_client: TestClient):
    response = api_client.patch(
        f"{GAME_TYPES_PREFIX}999",
        json={"name": GameTypeChoices.WHOS_MOST_LIKELY},
    )
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_update_game_type_invalid_name(api_client: TestClient):
    game_type = GameTypeFactory.create()

    response = api_client.patch(
        f"{GAME_TYPES_PREFIX}{game_type.id}",
        json={"name": "not from enum"},
    )
    assert response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY, response.text


def test_delete_game_type(api_client: TestClient):
    game_type = GameTypeFactory.create()
    response = api_client.delete(f"{GAME_TYPES_PREFIX}{game_type.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    response = api_client.get(f"{GAME_TYPES_PREFIX}{game_type.id}")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text


def test_delete_non_existing_game_type(api_client: TestClient):
    response = api_client.delete(f"{GAME_TYPES_PREFIX}999")
    assert response.status_code == status.HTTP_404_NOT_FOUND, response.text
