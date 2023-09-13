from collections.abc import Generator

import pytest
from httpx import Response
from starlette import status

from domuwa.models import Question
from domuwa.tests.setup import client, override_get_db
from domuwa.tests.data_for_testing import (
    AnswerValid, TEST_ANSWERS_INVALID, TEST_ANSWERS_VALID, TEST_QUESTIONS_VALID, AUTHOR, TEXT, QUESTION_ID, CORRECT, ID)

ANSWERS_PREFIX = "/answer/"
QUESTIONS_PREFIX = "/question/"

ResponseType = dict[str, str | int | float | bool]


# TODO: not a fixture for each test, but at the start of the answer's tests
@pytest.fixture
def get_mock_question(test_question_idx: int) -> Generator[Question, None]:
    test_question = TEST_QUESTIONS_VALID[test_question_idx]
    db_question = Question(
        game_name=test_question.game_name,
        category=test_question.category,
        author=test_question.author,
        text=test_question.text,
        excluded=test_question.excluded,
    )
    db = next(override_get_db())
    db.add(db_question)
    db.commit()
    db.refresh(db_question)
    yield db_question

    db.delete(db_question)
    db.commit()


@pytest.fixture
def get_mock_questions(questions_idxs: list[int]) -> Generator[list[Question], None]:
    questions = []
    db = next(override_get_db())
    for question_idx in questions_idxs:
        test_question = TEST_QUESTIONS_VALID[question_idx]
        db_question = Question(
            game_name=test_question.game_name,
            category=test_question.category,
            author=test_question.author,
            text=test_question.text,
            excluded=test_question.excluded,
        )
        db.add(db_question)
        db.commit()
        db.refresh(db_question)
        questions.append(db_question)
    yield questions

    for question in questions:
        db.delete(question)
        db.commit()


def validate_response(request_data: ResponseType, response_data: ResponseType) -> None:
    assert request_data[AUTHOR] == response_data[AUTHOR]
    assert request_data[TEXT] == request_data[TEXT]
    assert request_data[QUESTION_ID] == response_data[QUESTION_ID]
    assert request_data[CORRECT] == response_data.get(CORRECT, False)


def assert_invalid_answer_data(invalid_key: str, expected_status: int) -> None:
    test_answer = TEST_ANSWERS_INVALID[invalid_key]
    answer_response = client.post(ANSWERS_PREFIX, params=test_answer.__dict__)
    assert answer_response.status_code == expected_status, answer_response.text


def create_valid_answer(valid_answer_idx: int, mock_question_idx: int) -> AnswerValid:
    answer = TEST_ANSWERS_VALID[valid_answer_idx]
    answer.add_question_id(mock_question_idx)
    return answer


def post_valid_answer(answer_data: dict) -> Response:
    answer_response = client.post(ANSWERS_PREFIX, params=answer_data)
    assert answer_response.status_code == status.HTTP_201_CREATED, answer_response.text
    return answer_response


@pytest.mark.parametrize("test_question_idx", [0])
def test_create_answer(get_mock_question, test_question_idx):
    mock_question = get_mock_question
    mock_question_id = mock_question.id
    answer = create_valid_answer(0, mock_question_id)
    answer_data = answer.__dict__
    answer_response = post_valid_answer(answer_data)

    response_data = answer_response.json()
    validate_response(answer_data, response_data)

    # test answer in db
    assert ID in response_data
    answer_id = response_data[ID]
    answer_response = client.get(ANSWERS_PREFIX + str(answer_id))
    assert answer_response.status_code == status.HTTP_200_OK, answer_response.text
    validate_response(answer_data, answer_response.json())

    # test answer appended to question
    db = next(override_get_db())
    db_question = db.get(Question, mock_question_id)
    assert answer_id in [answer.id for answer in db_question.answers]


@pytest.mark.parametrize("test_question_idx", [0])
def test_create_answer_invalid_author(get_mock_question, test_question_idx):
    assert_invalid_answer_data(AUTHOR, status.HTTP_400_BAD_REQUEST)


@pytest.mark.parametrize("test_question_idx", [0])
def test_create_answer_invalid_text(get_mock_question, test_question_idx):
    assert_invalid_answer_data(TEXT, status.HTTP_400_BAD_REQUEST)


@pytest.mark.parametrize("test_question_idx", [0])
def test_create_answer_invalid_question_id(get_mock_question, test_question_idx):
    assert_invalid_answer_data(QUESTION_ID, status.HTTP_404_NOT_FOUND)


@pytest.mark.parametrize("test_question_idx", [0])
def test_create_answer_invalid_correct(get_mock_question, test_question_idx):
    assert_invalid_answer_data(CORRECT, status.HTTP_422_UNPROCESSABLE_ENTITY)  # cannot convert to bool


@pytest.mark.parametrize("test_question_idx", [0])
def test_create_answer_correct_answer_already_exists(get_mock_question, test_question_idx):
    mock_question = get_mock_question
    mock_question_id = mock_question.id

    correct_answer1 = create_valid_answer(1, mock_question_id)
    post_valid_answer(correct_answer1.__dict__)

    correct_answer2 = TEST_ANSWERS_VALID[2]
    correct_answer2.add_question_id(mock_question_id)
    correct_answer2_response = client.post(ANSWERS_PREFIX, params=correct_answer2.__dict__)
    assert correct_answer2_response.status_code == status.HTTP_400_BAD_REQUEST, correct_answer2_response.text


@pytest.mark.parametrize("test_question_idx", [0])
def test_get_answer_invalid_id(get_mock_question, test_question_idx):
    answer_response = client.get(ANSWERS_PREFIX + str(-1))
    assert answer_response.status_code == status.HTTP_404_NOT_FOUND, answer_response.text


@pytest.mark.parametrize("questions_idxs", [[0, 1]])
def test_get_all_answers(get_mock_questions, questions_idxs):
    # TODO: finish test
    mock_question1, mock_question2 = get_mock_questions
    assert True


@pytest.mark.parametrize("test_question_idx", [0])
def test_get_answers_for_question(get_mock_question, test_question_idx):
    mock_question = get_mock_question
    mock_question_id = mock_question.id

    correct_answer1 = create_valid_answer(0, mock_question_id)
    correct_answer1_response = post_valid_answer(correct_answer1.__dict__)
    correct_answer1_response_data = correct_answer1_response.json()

    correct_answer2 = create_valid_answer(1, mock_question_id)
    correct_answer2_response = post_valid_answer(correct_answer2.__dict__)
    correct_answer2_response_data = correct_answer2_response.json()

    answers_response = client.get(f"{ANSWERS_PREFIX}for_question/{mock_question_id}")
    assert answers_response.status_code == status.HTTP_200_OK, answers_response.text
    answers_response_data = answers_response.json()
    assert isinstance(answers_response_data, list)
    answer_response1_data, answer_response2_data = answers_response_data

    assert ID in answer_response1_data
    assert answer_response1_data[ID] == correct_answer1_response_data[ID]
    validate_response(correct_answer1_response_data, answer_response1_data)

    assert ID in answer_response2_data
    assert answer_response2_data[ID] == correct_answer2_response_data[ID]
    validate_response(correct_answer2_response_data, answer_response2_data)


def test_get_answers_for_question_invalid_question_id():
    answer_response = client.get(f"{ANSWERS_PREFIX}for_question/-1")
    assert answer_response.status_code == status.HTTP_200_OK, answer_response.text
    answer_response_data = answer_response.json()
    assert isinstance(answer_response_data, list)
    assert not answer_response_data  # empty list

# def test_update_answer():
#     pass
#
#
# def test_update_answer_invalid_id():
#     pass
#
#
# def test_update_answer_invalid_author():
#     pass
#
#
# def test_update_answer_invalid_text():
#     pass
#
#
# def test_update_answer_invalid_question_id():
#     pass
#
#
# def test_update_answer_invalid_correct():
#     pass
#
#
# def test_update_answer_correct_answer_already_exists():
#     pass
#
#
# def test_delete_answer():
#     pass
