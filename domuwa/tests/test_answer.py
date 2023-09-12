from collections.abc import Generator

import pytest
from starlette import status

from domuwa.tests.setup import client
from domuwa.tests.data_for_testing import (
    ANSWER_ID, TEST_ANSWERS_INVALID, TEST_ANSWERS_VALID, TEST_QUESTIONS_VALID, AUTHOR, TEXT, QUESTION_ID, CORRECT, ID)

ANSWERS_PREFIX = "/answer/"
QUESTIONS_PREFIX = "/question/"

ResponseType = dict[str, str | int | float | bool]


@pytest.fixture
def get_mock_question(test_question_idx: int) -> Generator[int, None]:
    test_question = TEST_QUESTIONS_VALID[test_question_idx]
    question_response = client.post(
        QUESTIONS_PREFIX,
        params=test_question
    )
    question_id = question_response.json()[ID]
    yield question_id

    client.delete(
        QUESTIONS_PREFIX,
        params={QUESTION_ID: question_id}
    )


def validate_response(request_data: ResponseType, response_data: ResponseType) -> None:
    assert request_data[AUTHOR] == response_data[AUTHOR]
    assert request_data[TEXT] == request_data[TEXT]
    assert request_data[QUESTION_ID] == response_data[QUESTION_ID]
    assert request_data[CORRECT] == response_data.get(CORRECT, False)


@pytest.mark.parametrize("test_question_idx", [0])
def test_create_answer(get_mock_question, test_question_idx):
    test_answer = TEST_ANSWERS_VALID[0]
    test_answer[QUESTION_ID] = get_mock_question
    answer_response = client.post(
        ANSWERS_PREFIX,
        params=test_answer
    )

    assert answer_response.status_code == status.HTTP_201_CREATED, answer_response.text
    data = answer_response.json()
    validate_response(data, test_answer)

    assert ID in data
    answer_id = data[ID]
    answer_response = client.get(ANSWERS_PREFIX + str(answer_id))
    assert answer_response.status_code == status.HTTP_200_OK, answer_response.text
    validate_response(answer_response.json(), test_answer)


def test_create_answer_invalid_author():
    pass


def test_create_answer_invalid_text():
    pass


def test_create_answer_invalid_correct():
    pass


def test_create_answer_invalid_question_id():
    pass


def test_get_answer():
    pass


def test_get_answer_invalid_id():
    pass


def test_get_answers_for_question():
    pass


def test_get_answers_for_question_invalid_question_id():
    pass


def test_get_all_answers():
    pass


def test_update_answer():
    pass


def test_update_answer_invalid_id():
    pass


def test_update_answer_invalid_author():
    pass


def test_update_answer_invalid_text():
    pass


def test_update_answer_invalid_correct():
    pass


def test_update_answer_invalid_question_id():
    pass


def test_delete_answer():
    pass
