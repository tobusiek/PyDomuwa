from collections.abc import Generator

import pytest
from starlette import status

from domuwa import models
from domuwa.services import game_rooms_services
from domuwa.tests import data_for_testing as test_data
from domuwa.tests import factories
from domuwa.tests import setup as tests_setup


class TestPlayerEndpoint:
    PLAYERS_PREFIX = "/player/"
    GAME_ROOMS_PREFIX = "/game_rooms/"

    def validate_response(
        self,
        request_data: test_data.ResponseType,
        response_data: test_data.ResponseType,
    ) -> None:
        assert request_data[test_data.NAME] == response_data[test_data.NAME]
        assert request_data[test_data.SCORE] == response_data[test_data.SCORE]

    # def post_valid_player(
    # valid_player_idx: int = 0,
    # ) -> Generator[test_data.ResponseType, None, None]:
    # yield player_factory.create(id=1)
    # player = test_data.TEST_PLAYERS_VALID[valid_player_idx]
    # player_data = player.__dict__
    # player_data.pop(test_data.SCORE, None)
    # player_response = tests_setup.client.post(
    #     PLAYERS_PREFIX,
    #     params=player_data,
    # )
    #
    # assert player_response.status_code == status.HTTP_201_CREATED, player_response.text
    # player_response_data = player_response.json()
    # assert test_data.ID in player_response_data
    # yield player_response_data
    #
    # db = next(tests_setup.override_get_db_session())
    # db_player = db.get(models.Player, player_response_data[test_data.ID])
    # if db_player is not None:
    #     db.delete(db_player)
    # db.commit()

    def test_create_player(self, player: factories.PlayerFactory) -> None:
        # player_data = next(post_valid_player())
        # player_id = player_data[test_data.ID]
        # player = player.build()
        player_response = tests_setup.client.post(self.PLAYERS_PREFIX, data=player)
        assert (
            player_response.status_code == status.HTTP_201_CREATED
        ), player_response.text

        player_response = tests_setup.client.get(self.PLAYERS_PREFIX + str(1))
        assert player_response.status_code == status.HTTP_200_OK, player_response.text

        player_response_data = player_response.json()
        # self.validate_response(player_data, player_response_data)

        assert test_data.GAMES_PLAYED in player_response_data, player_response_data
        assert player_response_data[test_data.GAMES_PLAYED] == 0, player_response_data
        assert test_data.GAMES_WON in player_response_data, player_response_data
        assert player_response_data[test_data.GAMES_WON] == 0, player_response_data

        # db = next(tests_setup.override_get_db_session())
        # db_player = db.get(models.Player, player_id)
        # self.validate_response(player_response_data, db_player.__dict__)

    # def test_create_player_invalid_name() -> None:
    #     invalid_player = test_data.TEST_PLAYERS_INVALID[test_data.NAME]
    #     player_response = tests_setup.client.post(
    #         PLAYERS_PREFIX,
    #         params=invalid_player.__dict__,
    #     )
    #     assert (
    #         player_response.status_code == status.HTTP_422_UNPROCESSABLE_ENTITY
    #     ), player_response.text
    #
    # def test_get_player_invalid_id() -> None:
    #     player_response = tests_setup.client.get(PLAYERS_PREFIX + str(999))
    #     assert (
    #         player_response.status_code == status.HTTP_404_NOT_FOUND
    #     ), player_response.text
    #
    # def test_get_all_players() -> None:
    #     db = next(tests_setup.override_get_db_session())
    #     db_players = db.query(models.Player).all()
    #     assert isinstance(db_players, list)
    #     assert len(db_players) == 0, "Db not empty"
    #
    #     player1_request_data = next(post_valid_player(0))
    #     player2_request_data = next(post_valid_player(1))
    #
    #     players_response = tests_setup.client.get(PLAYERS_PREFIX)
    #     assert players_response.status_code == status.HTTP_200_OK, players_response.text
    #     players_response_data = players_response.json()
    #     assert isinstance(players_response_data, list)
    #     assert len(players_response_data) == 2, players_response_data
    #
    #     player1_response_data, player2_response_data = players_response_data
    #     validate_response(player1_request_data, player1_response_data)
    #     validate_response(player2_request_data, player2_response_data)
    #
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
