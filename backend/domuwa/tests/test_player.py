from collections.abc import Callable, Generator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.orm import Session
from starlette import status

from domuwa import schemas
from domuwa.models import Player
from domuwa.tests.factories import PlayerFactory


class TestPlayerEndpoint:
    PLAYERS_PREFIX = "/api/player/"
    GAME_ROOMS_PREFIX = "/api/game_rooms/"

    @pytest.fixture()
    def player(
        self,
        player_factory: PlayerFactory,
        db_session: Session,
    ) -> Generator[Player, None, None]:
        player = player_factory.create()

        db_session.add(player)
        db_session.commit()

        yield player

        db_session.delete(player)
        db_session.commit()

    @pytest.fixture()
    def players_creator(
        self,
        player_factory: PlayerFactory,
        db_session: Session,
    ) -> Callable[[int], Generator[list[Player], None, None]]:
        def _players(
            count: int = 3,
        ) -> Generator[list[Player], None, None]:
            players = player_factory.create_batch(count)

            for idx, player in enumerate(players):
                db_session.add(player)
                db_session.commit()
                db_session.refresh(player)
                players[idx] = player

            yield players

            for player in players:
                db_session.delete(player)
            db_session.commit()

        return _players

    def assert_valid_response(self, response: dict[str, Any]) -> None:
        assert "id" in response, response
        assert "games_played" in response, response
        assert "games_won" in response, response
        assert "score" in response, response

    def test_create_player(
        self,
        player_factory: PlayerFactory,
        api_client: TestClient,
    ) -> None:
        player = schemas.PlayerCreateSchema.model_validate(player_factory.build())

        response = api_client.post(
            self.PLAYERS_PREFIX,
            params=player.model_dump(),
        )
        assert response.status_code == status.HTTP_201_CREATED, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)

        response = api_client.get(
            f"{self.PLAYERS_PREFIX}{response_data['id']}",
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        self.assert_valid_response(response.json())

    def test_create_player_invalid_name(self, api_client: TestClient) -> None:
        player = {"name": 12}

        response = api_client.post(self.PLAYERS_PREFIX, params=player)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    def test_create_player_non_unique_name(
        self,
        player: Player,
        api_client: TestClient,
    ) -> None:
        new_player = {"name": player.name}

        response = api_client.post(self.PLAYERS_PREFIX, params=new_player)
        assert response.status_code == status.HTTP_400_BAD_REQUEST, response.text

    def test_get_non_existing_player(self, api_client: TestClient) -> None:
        player_response = api_client.get(self.PLAYERS_PREFIX + str(999))
        assert (
            player_response.status_code == status.HTTP_404_NOT_FOUND
        ), player_response.text

    def test_get_all_players(
        self,
        players_creator: Callable[[int], list[Player]],
        api_client: TestClient,
        count: int = 3,
    ) -> None:
        players_creator(count)
        response = api_client.get(self.PLAYERS_PREFIX)
        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) >= count, response.text

    # @pytest.mark.asyncio()
    # async def test_get_all_players_from_game_room() -> None:
    #     db = next(tests_setup.override_get_db_session())
    #     game_room = models.GameRoom(game_name="ego", game_category="SFW")
    #     db.add(game_room)
    #     db.commit()
    #     db.refresh(game_room)
    #     game_room_id = game_room.id
    #
    #     player1_request_data = next(post_valid_player(0))
    #     player2_request_data = next(post_valid_player(1))
    #
    #     await game_rooms_services.add_player(
    #         game_room_id,
    #         player1_request_data[test_data.ID],  # type: ignore
    #         db,
    #     )
    #     await game_rooms_services.add_player(
    #         game_room_id,
    #         player2_request_data[test_data.ID],  # type: ignore
    #         db,
    #     )
    #
    #     players_response = tests_setup.client.get(
    #         PLAYERS_PREFIX + "from_game_room/" + str(game_room.id),
    #     )
    #     assert players_response.status_code == status.HTTP_200_OK, players_response.text
    #
    #     players_response_data = players_response.json()
    #     assert isinstance(players_response_data, list), players_response_data
    #     assert len(players_response_data) == 2, players_response_data
    #
    #     player1_response_data, player2_response_data = players_response_data
    #     validate_response(player1_request_data, player1_response_data)
    #     validate_response(player2_request_data, player2_response_data)
    #
    #     db.delete(game_room)
    #     db.commit()
    #     db.close()
    #
    # def test_get_all_players_from_game_room_invalid_id() -> None:
    #     players_response = tests_setup.client.get(
    #         PLAYERS_PREFIX + "from_game_room/" + str(999),
    #     )
    #     assert players_response.status_code == status.HTTP_200_OK, players_response.text
    #
    #     players_response_data = players_response.json()
    #     assert isinstance(players_response_data, list), players_response_data
    #     assert len(players_response_data) == 0, players_response_data
    #
    # def test_update_player_name() -> None:
    #     player_data = next(post_valid_player())
    #     player_id = player_data[test_data.ID]
    #
    #     updated_name = "updated name"
    #     player_response = tests_setup.client.put(
    #         PLAYERS_PREFIX + "update_name/",
    #         params={test_data.PLAYER_ID: player_id, "new_name": updated_name},
    #     )
    #     assert player_response.status_code == status.HTTP_200_OK, player_response.text
    #
    #     player_response_data = player_response.json()
    #     assert test_data.ID in player_response_data, player_response_data
    #     assert player_response_data[test_data.ID] == player_id
    #     assert player_response_data[test_data.NAME] == updated_name
    #
    # def test_update_player_name_invalid_id() -> None:
    #     next(post_valid_player())
    #
    #     player_response = tests_setup.client.put(
    #         PLAYERS_PREFIX + "update_name/",
    #         params={test_data.PLAYER_ID: -1, "new_name": "valid name"},
    #     )
    #     assert (
    #         player_response.status_code == status.HTTP_404_NOT_FOUND
    #     ), player_response.text
    #
    # def test_update_player_name_invalid_name() -> None:
    #     player_data = next(post_valid_player())
    #     player_id = player_data[test_data.ID]
    #
    #     player_response = tests_setup.client.put(
    #         PLAYERS_PREFIX + "update_name/",
    #         params={test_data.PLAYER_ID: player_id, "new_name": ""},
    #     )
    #     assert (
    #         player_response.status_code == status.HTTP_400_BAD_REQUEST
    #     ), player_response.text
    #
    # def test_update_player_score() -> None:
    #     player_data = next(post_valid_player())
    #     player_id = player_data[test_data.ID]
    #
    #     player_response = tests_setup.client.put(
    #         PLAYERS_PREFIX + "update_score/",
    #         params={test_data.PLAYER_ID: player_id, "points": 1},
    #     )
    #     assert player_response.status_code == status.HTTP_200_OK, player_response.text
    #     player_response_data = player_response.json()
    #
    #     assert test_data.SCORE in player_response_data, player_response_data
    #     assert (
    #         int(player_data[test_data.SCORE]) + 1
    #         == player_response_data[test_data.SCORE]
    #     ), player_response_data
    #
    # def test_update_player_score_invalid_player_id() -> None:
    #     next(post_valid_player())
    #
    #     player_response = tests_setup.client.put(
    #         PLAYERS_PREFIX + "update_score/",
    #         params={test_data.PLAYER_ID: -1, "points": 1},
    #     )
    #     assert (
    #         player_response.status_code == status.HTTP_404_NOT_FOUND
    #     ), player_response.text
    #
    # def test_update_player_score_invalid_score() -> None:
    #     player_data = next(post_valid_player())
    #     player_id = player_data[test_data.ID]
    #
    #     player_response = tests_setup.client.put(
    #         PLAYERS_PREFIX + "update_score/",
    #         params={test_data.PLAYER_ID: player_id, "points": "five"},
    #     )
    #     assert (
    #         player_response.status_code == status.HTTP_400_BAD_REQUEST
    #     ), player_response.text
    #
    # def test_reset_player_score() -> None:
    #     player_data = next(post_valid_player())
    #     player_id = player_data[test_data.ID]
    #
    #     player_response = tests_setup.client.put(
    #         PLAYERS_PREFIX + "reset_score/",
    #         params={test_data.PLAYER_ID: player_id},
    #     )
    #     assert player_response.status_code == status.HTTP_200_OK, player_response.text
    #     player_response_data = player_response.json()
    #
    #     assert test_data.SCORE in player_response_data, player_response_data
    #     assert player_response_data[test_data.SCORE] == 0, player_response_data
    #
    # def test_reset_player_score_invalid_player_id() -> None:
    #     next(post_valid_player())
    #
    #     player_response = tests_setup.client.put(
    #         PLAYERS_PREFIX + "reset_score/",
    #         params={test_data.PLAYER_ID: -1},
    #     )
    #     assert (
    #         player_response.status_code == status.HTTP_404_NOT_FOUND
    #     ), player_response.text
    #
    # def test_delete_player() -> None:
    #     player_data = next(post_valid_player())
    #     player_id = player_data[test_data.ID]
    #
    #     player_response = tests_setup.client.delete(
    #         PLAYERS_PREFIX + "delete/",
    #         params={test_data.PLAYER_ID: player_id},
    #     )
    #     assert (
    #         player_response.status_code == status.HTTP_204_NO_CONTENT
    #     ), player_response.text
    #
    # def test_delete_player_invalid_player_id() -> None:
    #     next(post_valid_player())
    #
    #     player_response = tests_setup.client.delete(
    #         PLAYERS_PREFIX + "delete/",
    #         params={test_data.PLAYER_ID: -1},
    #     )
    #     assert (
    #         player_response.status_code == status.HTTP_404_NOT_FOUND
    #     ), player_response.text
