from typing import Any

from fastapi import status
from fastapi.testclient import TestClient

from domuwa.tests.factories import GameTypeFactory

GAME_TYPES_PREFIX = "/api/game-types/"


def assert_valid_response(response: dict[str, Any]):
    assert "id" in response, response
    assert "name" in response, response


def test_create_game_type(api_client: TestClient):
    response = api_client.post(
        GAME_TYPES_PREFIX,
        json={"name": "Ego"},
    )
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    assert_valid_response(response_data)

    response = api_client.get(f'{GAME_TYPES_PREFIX}{response_data["id"]}')
    assert response.status_code == status.HTTP_200_OK, response.text
    assert_valid_response(response.json())


def test_create_game_type_invalid_name(api_client: TestClient):
    response = api_client.post(GAME_TYPES_PREFIX)
