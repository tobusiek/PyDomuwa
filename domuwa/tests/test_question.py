from collections.abc import Generator

from starlette import status

from domuwa.models import Question
from domuwa.tests.data_for_testing import (
    AUTHOR, CATEGORY,
    EXCLUDED, GAME_NAME, ID, TEST_QUESTIONS_VALID,
    ResponseType, TEXT,
)
from domuwa.tests.setup import client, override_get_db

QUESTIONS_PREFIX = "/question/"


def post_valid_question(valid_question_idx: int) -> Generator[Question, None]:
    question = TEST_QUESTIONS_VALID[valid_question_idx]
    question_response = client.post(QUESTIONS_PREFIX, params=question.__dict__)
    assert question_response.status_code == status.HTTP_201_CREATED, question_response.text
    question_response_data = question_response.json()
    assert ID in question_response_data
    yield question_response_data

    db = next(override_get_db())
    db.get(Question, question_response_data[ID]).delete()
    db.commit()


def validate_response(request_data: ResponseType, response_data: ResponseType) -> None:
    assert request_data[GAME_NAME] == response_data[GAME_NAME]
    assert request_data[CATEGORY] == response_data[CATEGORY]
    assert request_data[AUTHOR] == response_data[AUTHOR]
    assert request_data[TEXT] == response_data[TEXT]
    assert request_data[EXCLUDED] == response_data[EXCLUDED]


def test_create_question() -> None:
    question_response_data = next(post_valid_question(0))
    question_id = question_response_data[ID]
    question_response = client.get(QUESTIONS_PREFIX + str(question_id))
    assert question_response.status_code == status.HTTP_200_OK, question_response.text
    validate_response(question_response_data, question_response.json())

    db = next(override_get_db())
    db_question = db.get(Question, question_response_data[ID])
    validate_response(question_response_data, db_question.__dict__)


def test_create_question_invalid_data() -> None:
    pass


def test_get_question_invalid_id() -> None:
    question_response = client.get(QUESTIONS_PREFIX + str(999))
    assert question_response.status_code == status.HTTP_404_NOT_FOUND, question_response.text


def test_get_all_questions() -> None:
    db = next(override_get_db())
    questions = db.query(Question).all()
    assert isinstance(questions, list)
    assert len(questions) == 0, "Db not empty"

    question1_request_data = next(post_valid_question(0))
    question2_request_data = next(post_valid_question(1))

    questions_response = client.get(QUESTIONS_PREFIX)
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
