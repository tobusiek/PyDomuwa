import json
from collections.abc import Generator

from starlette import status

from domuwa import models
from domuwa.tests import data_for_testing as test_data
from domuwa.tests import setup as tests_setup

QUESTIONS_PREFIX = "/question/"


def post_valid_question(valid_question_idx: int) -> Generator[dict, None, None]:
    question = test_data.TEST_QUESTIONS_VALID[valid_question_idx]
    question_response = tests_setup.client.post(
        QUESTIONS_PREFIX,
        params=question.__dict__,
    )
    assert (
        question_response.status_code == status.HTTP_201_CREATED
    ), question_response.text
    question_response_data = question_response.json()
    assert test_data.ID in question_response_data
    yield question_response_data

    db = next(tests_setup.override_get_db_session())
    db_question = db.get(models.Question, question_response_data[test_data.ID])
    if db_question is not None:
        db.delete(db_question)
    db.commit()


def validate_response(
    request_data: test_data.ResponseType,
    response_data: test_data.ResponseType,
) -> None:
    assert request_data[test_data.GAME_NAME] == response_data[test_data.GAME_NAME]
    assert request_data[test_data.CATEGORY] == response_data[test_data.CATEGORY]
    assert request_data[test_data.AUTHOR] == response_data[test_data.AUTHOR]
    assert request_data[test_data.TEXT] == response_data[test_data.TEXT]
    assert request_data[test_data.EXCLUDED] == response_data[test_data.EXCLUDED]


def put_invalid_question(
    invalid_key: str,
    question_id: int,
    expected_status: int = status.HTTP_400_BAD_REQUEST,
) -> None:
    invalid_question = test_data.TEST_QUESTIONS_INVALID[invalid_key]
    invalid_question.add_id(question_id)
    invalid_question_response = tests_setup.client.put(
        QUESTIONS_PREFIX,
        params=invalid_question.__dict__,
    )
    assert (
        invalid_question_response.status_code == expected_status
    ), invalid_question_response.text


def test_create_question() -> None:
    question_response_data = next(post_valid_question(0))
    question_id = question_response_data[test_data.ID]
    question_response = tests_setup.client.get(QUESTIONS_PREFIX + str(question_id))
    assert question_response.status_code == status.HTTP_200_OK, question_response.text
    validate_response(question_response_data, question_response.json())

    db = next(tests_setup.override_get_db_session())
    db_question = db.get(models.Question, question_response_data[test_data.ID])
    validate_response(question_response_data, db_question.__dict__)


def test_create_question_invalid_data() -> None:
    invalid_question = test_data.TEST_QUESTIONS_INVALID[test_data.GAME_NAME]
    question_response = tests_setup.client.post(
        QUESTIONS_PREFIX,
        params=invalid_question.__dict__,
    )
    assert (
        question_response.status_code == status.HTTP_400_BAD_REQUEST
    ), question_response.text


def test_get_question_invalid_id() -> None:
    question_response = tests_setup.client.get(QUESTIONS_PREFIX + str(999))
    assert (
        question_response.status_code == status.HTTP_404_NOT_FOUND
    ), question_response.text


def test_get_all_questions() -> None:
    db = next(tests_setup.override_get_db_session())
    questions = db.query(models.Question).all()
    assert isinstance(questions, list)
    assert len(questions) == 0, "Db not empty"

    question1_request_data = next(post_valid_question(0))
    question2_request_data = next(post_valid_question(1))

    questions_response = tests_setup.client.get(QUESTIONS_PREFIX)
    assert questions_response.status_code == status.HTTP_200_OK, questions_response.text
    questions_response_data = questions_response.json()
    assert isinstance(questions_response_data, list)
    assert len(questions_response_data) == 2, questions_response_data

    question1_response_data, question2_response_data = questions_response_data
    validate_response(question1_request_data, question1_response_data)
    validate_response(question2_request_data, question2_response_data)


def test_update_question() -> None:
    question_data = next(post_valid_question(0))

    updated_question = test_data.TEST_QUESTIONS_VALID[0]
    updated_question.add_id(question_data[test_data.ID])
    updated_question.excluded = not updated_question.excluded

    updated_question_put_response = tests_setup.client.put(
        QUESTIONS_PREFIX,
        params=updated_question.__dict__,
    )
    updated_question_put_response_data = updated_question_put_response.json()
    assert (
        test_data.ID in updated_question_put_response_data
    ), updated_question_put_response.text

    updated_question_get_response = tests_setup.client.get(
        QUESTIONS_PREFIX + str(question_data[test_data.ID]),
    )
    updated_question_get_response_data = updated_question_get_response.json()
    assert (
        test_data.ID in updated_question_get_response_data
    ), updated_question_get_response.text
    validate_response(
        updated_question_put_response_data,
        updated_question_get_response_data,
    )


def test_update_question_invalid_data() -> None:
    correct_question_data = next(post_valid_question(0))
    question_id = correct_question_data[test_data.ID]

    invalid_id_question = correct_question_data.copy()
    invalid_id_question[test_data.QUESTION_ID] = correct_question_data.pop(test_data.ID)
    invalid_id_question[test_data.QUESTION_ID] = -1
    invalid_id_question_response = tests_setup.client.put(
        QUESTIONS_PREFIX,
        params=invalid_id_question,
    )
    assert (
        invalid_id_question_response.status_code == status.HTTP_404_NOT_FOUND
    ), invalid_id_question_response.text + json.dumps(invalid_id_question)

    put_invalid_question(test_data.GAME_NAME, question_id)
    put_invalid_question(test_data.CATEGORY, question_id)
    put_invalid_question(test_data.AUTHOR, question_id)
    put_invalid_question(test_data.TEXT, question_id)
    put_invalid_question(
        test_data.EXCLUDED,
        question_id,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    )


def test_delete_question() -> None:
    question_data = next(post_valid_question(0))
    question_id = question_data[test_data.ID]

    delete_response = tests_setup.client.delete(
        QUESTIONS_PREFIX,
        params={test_data.QUESTION_ID: question_id},
    )
    assert (
        delete_response.status_code == status.HTTP_204_NO_CONTENT
    ), delete_response.text

    question_response = tests_setup.client.get(QUESTIONS_PREFIX + str(question_id))
    assert (
        question_response.status_code == status.HTTP_404_NOT_FOUND
    ), question_response.text


def test_delete_question_invalid_id() -> None:
    invalid_id = 999
    get_response = tests_setup.client.get(QUESTIONS_PREFIX + str(invalid_id))
    assert get_response.status_code == status.HTTP_404_NOT_FOUND, get_response.text
    delete_response = tests_setup.client.delete(
        QUESTIONS_PREFIX,
        params={test_data.QUESTION_ID: invalid_id},
    )
    assert (
        delete_response.status_code == status.HTTP_404_NOT_FOUND
    ), delete_response.text
