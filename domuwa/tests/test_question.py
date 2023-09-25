from starlette import status

from domuwa.tests.data_for_testing import (
    AUTHOR,
    CATEGORY,
    EXCLUDED,
    GAME_NAME,
    ID,
    TEST_QUESTIONS_VALID,
    TEXT,
    ResponseType,
)
from domuwa.tests.setup import client

QUESTIONS_PREFIX = "/question/"


def validate_response(request_data: ResponseType, response_data: ResponseType) -> None:
    assert request_data[GAME_NAME] == response_data[GAME_NAME]
    assert request_data[CATEGORY] == response_data[CATEGORY]
    assert request_data[AUTHOR] == response_data[AUTHOR]
    assert request_data[TEXT] == response_data[TEXT]
    assert request_data[EXCLUDED] == response_data[EXCLUDED]


def test_create_question() -> None:
    question = TEST_QUESTIONS_VALID[0]
    question_data = question.__dict__
    question_response = client.post(QUESTIONS_PREFIX, params=question_data)
    assert question_response.status_code == status.HTTP_201_CREATED, question_response.text
    question_response_data = question_response.json()

    assert ID in question_response_data
    question_id = question_response_data[ID]
    question_response = client.get(QUESTIONS_PREFIX + str(question_id))
    assert question_response.status_code == status.HTTP_200_OK, question_response.text
    validate_response(question_response_data, question_response.json())


def test_create_question_invalid_data() -> None:
    pass


def test_get_question() -> None:
    pass


def test_get_question_invalid_id() -> None:
    pass


def test_get_all_questions() -> None:
    pass


def test_update_question() -> None:
    pass


def test_update_question_invalid_data() -> None:
    pass


def test_delete_question() -> None:
    pass
