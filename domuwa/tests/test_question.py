from collections.abc import Generator

from starlette import status

from domuwa import models
from domuwa.tests import data_for_testing as test_data
from domuwa.tests import setup as tests_setup

QUESTIONS_PREFIX = "/question/"


def post_valid_question(valid_question_idx: int) -> Generator[dict, None, None]:
    question = test_data.TEST_QUESTIONS_VALID[valid_question_idx]
    question_response = tests_setup.client.post(
        QUESTIONS_PREFIX, params=question.__dict__,
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
    request_data: test_data.ResponseType, response_data: test_data.ResponseType,
) -> None:
    assert request_data[test_data.GAME_NAME] == response_data[test_data.GAME_NAME]
    assert request_data[test_data.CATEGORY] == response_data[test_data.CATEGORY]
    assert request_data[test_data.AUTHOR] == response_data[test_data.AUTHOR]
    assert request_data[test_data.TEXT] == response_data[test_data.TEXT]
    assert request_data[test_data.EXCLUDED] == response_data[test_data.EXCLUDED]


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
        QUESTIONS_PREFIX, params=invalid_question.__dict__,
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
    pass


def test_update_question_invalid_data() -> None:
    pass


def test_delete_question() -> None:
    pass
