from collections.abc import Generator

import httpx
import pytest
from sqlalchemy import orm
from starlette import status

from domuwa import models
from domuwa.tests import data_for_testing as test_data
from domuwa.tests import setup as tests_setup

ANSWERS_PREFIX = "/answer/"
QUESTIONS_PREFIX = "/question/"


def create_mock_question(
    test_question_idx: int,
    db_sess: orm.Session,
) -> models.Question:
    test_question = test_data.TEST_QUESTIONS_VALID[test_question_idx]
    db_question = models.Question(
        game_name=test_question.game_name,
        category=test_question.category,
        author=test_question.author,
        text=test_question.text,
        excluded=test_question.excluded,
    )
    db_sess.add(db_question)
    db_sess.commit()
    db_sess.refresh(db_question)
    return db_question


# TODO: not a fixture for each test, but at the start of the answer's tests (if possible)
@pytest.fixture()
def mock_question(question_idx: int) -> Generator[models.Question, None, None]:
    db = next(tests_setup.override_get_db_session())
    db_question = create_mock_question(question_idx, db)
    yield db_question
    db.delete(db_question)
    db.commit()


@pytest.fixture()
def mock_questions(
    questions_idxs: list[int],
) -> Generator[list[models.Question], None, None]:
    questions = []
    db = next(tests_setup.override_get_db_session())
    for question_idx in questions_idxs:
        db_question = create_mock_question(question_idx, db)
        questions.append(db_question)
    yield questions
    for question in questions:
        db.delete(question)
        db.commit()


def validate_response(
    request_data: test_data.ResponseType,
    response_data: test_data.ResponseType,
) -> None:
    assert request_data[test_data.AUTHOR] == response_data[test_data.AUTHOR]
    assert request_data[test_data.TEXT] == request_data[test_data.TEXT]
    assert request_data[test_data.QUESTION_ID] == response_data[test_data.QUESTION_ID]
    assert request_data[test_data.CORRECT] == response_data.get(
        test_data.CORRECT,
        False,
    )


def assert_invalid_answer_data(invalid_key: str, expected_status: int) -> None:
    test_answer = test_data.TEST_ANSWERS_INVALID[invalid_key]
    answer_response = tests_setup.client.post(
        ANSWERS_PREFIX,
        params=test_answer.__dict__,
    )
    assert answer_response.status_code == expected_status, answer_response.text


def create_valid_answer(
    valid_answer_idx: int,
    mock_question_id: int,
) -> test_data.AnswerValid:
    answer = test_data.TEST_ANSWERS_VALID[valid_answer_idx]
    answer.add_question_id(mock_question_id)
    return answer


def post_valid_answer(answer_data: dict) -> httpx.Response:
    answer_response = tests_setup.client.post(ANSWERS_PREFIX, params=answer_data)
    assert answer_response.status_code == status.HTTP_201_CREATED, answer_response.text
    answer_response_data = answer_response.json()
    validate_response(answer_data, answer_response_data)
    assert test_data.ID in answer_response_data
    return answer_response


def put_invalid_answer(
    invalid_key: str,
    answer_id: int,
    question_id: int | None = None,
    expected_status: int = status.HTTP_400_BAD_REQUEST,
) -> None:
    invalid_answer = test_data.TEST_ANSWERS_INVALID[invalid_key]
    invalid_answer.add_answer_id(answer_id)
    if question_id:
        invalid_answer.question_id = question_id
    invalid_text_answer_response = tests_setup.client.put(
        ANSWERS_PREFIX,
        params=invalid_answer.__dict__,
    )
    assert invalid_text_answer_response.status_code == expected_status


@pytest.mark.parametrize("question_idx", [0])
def test_create_answer(mock_question: models.Question, question_idx: int) -> None:
    mock_question_id = mock_question.id
    answer = create_valid_answer(0, mock_question_id)
    answer_data = answer.__dict__
    answer_response = post_valid_answer(answer_data)
    response_data = answer_response.json()

    assert test_data.ID in response_data
    answer_id = response_data[test_data.ID]
    answer_response = tests_setup.client.get(ANSWERS_PREFIX + str(answer_id))
    assert answer_response.status_code == status.HTTP_200_OK, answer_response.text
    validate_response(answer_data, answer_response.json())

    db = next(tests_setup.override_get_db_session())
    db_question = db.get(models.Question, mock_question_id)
    assert db_question is not None
    assert answer_id in [answer.id for answer in db_question.answers]


@pytest.mark.parametrize("question_idx", [0])
def test_create_answer_invalid_data(
    mock_question: models.Question,
    question_idx: int,
) -> None:
    assert_invalid_answer_data(test_data.AUTHOR, status.HTTP_400_BAD_REQUEST)
    assert_invalid_answer_data(test_data.TEXT, status.HTTP_400_BAD_REQUEST)
    assert_invalid_answer_data(test_data.QUESTION_ID, status.HTTP_404_NOT_FOUND)
    assert_invalid_answer_data(
        test_data.CORRECT,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    )  # cannot convert to bool


@pytest.mark.parametrize("question_idx", [0])
def test_create_answer_correct_answer_already_exists(
    mock_question: models.Question,
    question_idx: int,
) -> None:
    mock_question_id = mock_question.id

    correct_answer1 = create_valid_answer(1, mock_question_id)
    post_valid_answer(correct_answer1.__dict__)

    correct_answer2 = test_data.TEST_ANSWERS_VALID[2]
    correct_answer2.add_question_id(mock_question_id)
    correct_answer2_response = tests_setup.client.post(
        ANSWERS_PREFIX,
        params=correct_answer2.__dict__,
    )
    assert (
        correct_answer2_response.status_code == status.HTTP_400_BAD_REQUEST
    ), correct_answer2_response.text


@pytest.mark.parametrize("question_idx", [0])
def test_get_answer_invalid_id(
    mock_question: models.Question,
    question_idx: int,
) -> None:
    answer_response = tests_setup.client.get(ANSWERS_PREFIX + str(-1))
    assert (
        answer_response.status_code == status.HTTP_404_NOT_FOUND
    ), answer_response.text


@pytest.mark.parametrize("questions_idxs", [[0, 1]])
def test_get_all_answers(
    mock_questions: list[models.Question],
    questions_idxs: list[int],
) -> None:
    empty_answers_response = tests_setup.client.get(ANSWERS_PREFIX)
    assert (
        empty_answers_response.status_code == status.HTTP_200_OK
    ), empty_answers_response.text
    empty_answers_response_data = empty_answers_response.json()
    assert isinstance(empty_answers_response_data, list)
    assert len(empty_answers_response_data) == 0

    mock_question1, mock_question2 = mock_questions
    mock_question1_id = mock_question1.id
    mock_question2_id = mock_question2.id

    correct_answer1 = create_valid_answer(0, mock_question1_id)
    correct_answer1_response = post_valid_answer(correct_answer1.__dict__)
    correct_answer1_response_data = correct_answer1_response.json()

    correct_answer2 = create_valid_answer(1, mock_question1_id)
    correct_answer2_response = post_valid_answer(correct_answer2.__dict__)
    correct_answer2_response_data = correct_answer2_response.json()

    correct_answer3 = create_valid_answer(2, mock_question2_id)
    correct_answer3_response = post_valid_answer(correct_answer3.__dict__)
    correct_answer3_response_data = correct_answer3_response.json()

    answers_response = tests_setup.client.get(ANSWERS_PREFIX)
    assert answers_response.status_code == status.HTTP_200_OK, answers_response.text
    answers_response_data = answers_response.json()
    assert isinstance(answers_response_data, list)
    assert len(answers_response_data) > 0, answers_response_data
    assert len(answers_response_data) == 3, answers_response_data
    answer1_response, answer2_response, answer3_response = answers_response_data

    assert test_data.ID in answer1_response
    assert answer1_response[test_data.ID] == correct_answer1_response_data[test_data.ID]
    validate_response(answer1_response, correct_answer1_response_data)

    assert test_data.ID in answer2_response
    assert answer2_response[test_data.ID] == correct_answer2_response_data[test_data.ID]
    validate_response(answer2_response, correct_answer2_response_data)

    assert test_data.ID in answer3_response
    assert answer3_response[test_data.ID] == correct_answer3_response_data[test_data.ID]
    validate_response(answer3_response, correct_answer3_response_data)


@pytest.mark.parametrize("question_idx", [0])
def test_get_answers_for_question(
    mock_question: models.Question,
    question_idx: int,
) -> None:
    mock_question_id = mock_question.id

    correct_answer1 = create_valid_answer(0, mock_question_id)
    correct_answer1_response = post_valid_answer(correct_answer1.__dict__)
    correct_answer1_response_data = correct_answer1_response.json()

    correct_answer2 = create_valid_answer(1, mock_question_id)
    correct_answer2_response = post_valid_answer(correct_answer2.__dict__)
    correct_answer2_response_data = correct_answer2_response.json()

    answers_response = tests_setup.client.get(
        f"{ANSWERS_PREFIX}for_question/{mock_question_id}",
    )
    assert answers_response.status_code == status.HTTP_200_OK, answers_response.text
    answers_response_data = answers_response.json()
    assert isinstance(answers_response_data, list)
    answer_response1_data, answer_response2_data = answers_response_data

    assert test_data.ID in answer_response1_data
    assert (
        answer_response1_data[test_data.ID]
        == correct_answer1_response_data[test_data.ID]
    )
    validate_response(correct_answer1_response_data, answer_response1_data)

    assert test_data.ID in answer_response2_data
    assert (
        answer_response2_data[test_data.ID]
        == correct_answer2_response_data[test_data.ID]
    )
    validate_response(correct_answer2_response_data, answer_response2_data)


def test_get_answers_for_question_invalid_question_id() -> None:
    answer_response = tests_setup.client.get(f"{ANSWERS_PREFIX}for_question/-1")
    assert answer_response.status_code == status.HTTP_200_OK, answer_response.text
    answer_response_data = answer_response.json()
    assert isinstance(answer_response_data, list)
    assert len(answer_response_data) == 0, answer_response_data


@pytest.mark.parametrize("question_idx", [0])
def test_update_answer(mock_question: models.Question, question_idx: int) -> None:
    mock_question_id = mock_question.id

    answer = create_valid_answer(0, mock_question_id)
    answer_response = post_valid_answer(answer.__dict__)
    answer_response_data = answer_response.json()

    updated_answer = test_data.AnswerValid(
        author="updated_user",
        text="updated_text",
        correct=not answer_response_data[test_data.CORRECT],
    )
    updated_answer.add_answer_id(answer_response_data[test_data.ID])
    updated_answer.add_question_id(mock_question_id)
    updated_answer_put_response = tests_setup.client.put(
        ANSWERS_PREFIX,
        params=updated_answer.__dict__,
    )
    updated_answer_put_response_data = updated_answer_put_response.json()
    assert test_data.ID in updated_answer_put_response_data

    updated_answer_get_response = tests_setup.client.get(
        ANSWERS_PREFIX + str(answer_response_data[test_data.ID]),
    )
    updated_answer_get_response_data = updated_answer_get_response.json()
    assert test_data.ID in updated_answer_get_response_data
    validate_response(
        updated_answer_put_response_data,
        updated_answer_get_response_data,
    )


@pytest.mark.parametrize("question_idx", [0])
def test_update_answer_invalid_data(
    mock_question: models.Question,
    question_idx: int,
) -> None:
    mock_question_id = mock_question.id

    correct_answer1 = create_valid_answer(1, mock_question_id)
    correct_answer1_response = post_valid_answer(correct_answer1.__dict__)
    correct_answer1_response_data = correct_answer1_response.json()
    answer_id = correct_answer1_response_data[test_data.ID]

    # invalid answer id
    invalid_id_answer = correct_answer1_response_data.copy()
    invalid_id_answer[test_data.ANSWER_ID] = -1
    del invalid_id_answer[test_data.QUESTION]
    invalid_id_answer_response = tests_setup.client.put(
        ANSWERS_PREFIX,
        params=invalid_id_answer,
    )
    assert (
        invalid_id_answer_response.status_code == status.HTTP_404_NOT_FOUND
    ), invalid_id_answer_response.text

    put_invalid_answer(
        test_data.AUTHOR,
        answer_id,
        question_id=mock_question_id,
    )  # invalid author
    put_invalid_answer(
        test_data.TEXT,
        answer_id,
        question_id=mock_question_id,
    )  # invalid text
    put_invalid_answer(
        test_data.CORRECT,
        answer_id,
        mock_question_id,
        status.HTTP_422_UNPROCESSABLE_ENTITY,
    )  # invalid correct

    # correct answer already exists
    correct_answer2 = create_valid_answer(0, mock_question_id)
    correct_answer2_response = post_valid_answer(correct_answer2.__dict__)
    correct_answer2_response_data = correct_answer2_response.json()
    correct_answer2_response_data[test_data.CORRECT] = True
    del correct_answer2_response_data[test_data.QUESTION]
    correct_answer2_id = correct_answer2_response_data.pop(test_data.ID)
    correct_answer2_response_data[test_data.ANSWER_ID] = correct_answer2_id
    correct_answer2_response = tests_setup.client.put(
        ANSWERS_PREFIX,
        params=correct_answer2_response_data,
    )
    assert (
        correct_answer2_response.status_code == status.HTTP_400_BAD_REQUEST
    ), correct_answer2_response.text


@pytest.mark.parametrize("question_idx", [0])
def test_delete_answer(mock_question: models.Question) -> None:
    mock_question_id = mock_question.id

    answer = create_valid_answer(0, mock_question_id)
    answer_response = post_valid_answer(answer.__dict__)
    answer_response_data = answer_response.json()
    answer_id = answer_response_data[test_data.ID]

    delete_response = tests_setup.client.delete(
        ANSWERS_PREFIX,
        params={"answer_id": answer_id},
    )
    assert (
        delete_response.status_code == status.HTTP_204_NO_CONTENT
    ), delete_response.text

    answer_response = tests_setup.client.get(ANSWERS_PREFIX + str(answer_id))
    assert (
        answer_response.status_code == status.HTTP_404_NOT_FOUND
    ), answer_response.text


def test_delete_answer_invalid_id() -> None:
    invalid_id = 999
    get_response = tests_setup.client.get(ANSWERS_PREFIX + str(invalid_id))
    assert get_response.status_code == status.HTTP_404_NOT_FOUND, get_response.text
    delete_response = tests_setup.client.delete(
        ANSWERS_PREFIX,
        params={"answer_id": invalid_id},
    )
    assert (
        delete_response.status_code == status.HTTP_404_NOT_FOUND
    ), delete_response.text
