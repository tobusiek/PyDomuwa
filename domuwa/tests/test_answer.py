from starlette import status

from domuwa.tests.setup import client
from domuwa.tests.data_for_testing import (
    TEST_ANSWERS_INVALID, TEST_ANSWERS_VALID, TEST_QUESTIONS_VALID, AUTHOR, TEXT, QUESTION_ID, CORRECT, ID)

ANSWERS_PREFIX = "/answer/"

ResponseType = dict[str, str | int | float | bool]


def validate_response(response_data: ResponseType, request_data: ResponseType) -> None:
    assert response_data[AUTHOR] == request_data[AUTHOR]
    assert response_data[TEXT] == request_data[TEXT]
    assert response_data[QUESTION_ID] == request_data[QUESTION_ID]
    assert response_data[CORRECT] == request_data.get(CORRECT, False)


def test_create_answer():
    test_answer = TEST_ANSWERS_VALID[0]
    response = client.post(
        ANSWERS_PREFIX,
        params=test_answer
    )
    assert response.status_code == status.HTTP_200_OK, response.text
    data = response.json()
    validate_response(data, test_answer)

    assert ID in data
    answer_id = data[ID]
    response = client.get(ANSWERS_PREFIX + str(answer_id))
    assert response.status_code == status.HTTP_200_OK, response.text
    validate_response(response.json(), test_answer)


def test_create_answer_invalid_question_id():
    pass


def test_create_answer_invalid_data():
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


def test_update_answer_invalid_data():
    pass


def test_delete_answer():
    pass
