from typing import Any

from fastapi import status
from fastapi.testclient import TestClient

from domuwa.models.answer import Answer
from tests.factories import (
    AnswerFactory,
    GameTypeFactory,
    PlayerFactory,
    QnACategoryFactory,
    QuestionFactory,
)

ANSWERS_PREFIX = "/api/answers/"
QUESTIONS_PREFIX = "/api/questions/"


def dump_answer(answer: Answer):
    answer_data = {
        "text": answer.text,
        "excluded": answer.excluded,
        "author_id": answer.author_id,
        "game_type_id": answer.game_type_id,
        "game_category_id": answer.game_category_id,
    }
    if answer.question_id is not None:
        answer_data["question_id"] = answer.question_id
    return answer_data


def assert_valid_response(response_data: dict[str, Any]):
    assert "id" in response_data, response_data
    assert "text" in response_data, response_data
    assert "excluded" in response_data, response_data
    assert "author" in response_data, response_data
    assert "game_type" in response_data, response_data
    assert "game_category" in response_data, response_data


def build_answer_without_question():
    author = PlayerFactory.create()
    game_type = GameTypeFactory.create()
    game_category = QnACategoryFactory.create()
    return AnswerFactory.build(
        author_id=author.id,
        game_type_id=game_type.id,
        game_category_id=game_category.id,
    )


def build_answer_with_question():
    author = PlayerFactory.create()
    game_type = GameTypeFactory.create()
    game_category = QnACategoryFactory.create()
    question = QuestionFactory.create(
        author_id=author.id,
        game_type_id=game_type.id,
        game_category_id=game_category.id,
    )
    return AnswerFactory.build(
        author_id=author.id,
        game_type_id=game_type.id,
        game_category_id=game_category.id,
        question_id=question.id,
    )


def create_answer_without_question():
    author = PlayerFactory.create()
    game_type = GameTypeFactory.create()
    game_category = QnACategoryFactory.create()
    return AnswerFactory.create(
        author_id=author.id,
        game_type_id=game_type.id,
        game_category_id=game_category.id,
    )


def create_answer_with_question():
    author = PlayerFactory.create()
    game_type = GameTypeFactory.create()
    game_category = QnACategoryFactory.create()
    question = QuestionFactory.create(
        author_id=author.id,
        game_type_id=game_type.id,
        game_category_id=game_category.id,
    )
    return AnswerFactory.create(
        author_id=author.id,
        game_type_id=game_type.id,
        game_category_id=game_category.id,
        question_id=question.id,
    )


def test_create_answer_with_question(api_client: TestClient):
    answer = build_answer_with_question()

    response = api_client.post(ANSWERS_PREFIX, json=dump_answer(answer))
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    assert_valid_response(response_data)

    response = api_client.get(f"{ANSWERS_PREFIX}{response_data['id']}")
    assert response.status_code == status.HTTP_200_OK, response.text
    answer_response_data = response.json()
    assert_valid_response(answer_response_data)

    response = api_client.get(f"{QUESTIONS_PREFIX}{answer.question_id}")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()

    assert "answers" in response_data, response_data
    answers = response_data["answers"]
    assert isinstance(answers, list), response_data
    assert len(answers) == 1, response_data
    answer_response_data.pop("question", None)
    assert answers[0] == answer_response_data


def test_create_answer_without_question(api_client: TestClient):
    answer = build_answer_without_question()

    response = api_client.post(ANSWERS_PREFIX, json=dump_answer(answer))
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    assert_valid_response(response_data)

    response = api_client.get(f"{ANSWERS_PREFIX}{response_data['id']}")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert_valid_response(response_data)


def test_get_answer_by_id(api_client: TestClient):
    answer = create_answer_without_question()

    response = api_client.get(f"{ANSWERS_PREFIX}{answer.id}")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert_valid_response(response_data)

    assert response_data["id"] == answer.id
    assert response_data["text"] == answer.text
    assert response_data["excluded"] == answer.excluded
    assert response_data["author"]["id"] == answer.author_id
    assert response_data["game_type"]["id"] == answer.game_type_id
    assert response_data["game_category"]["id"] == answer.game_category_id


def test_get_all_answers(api_client: TestClient, answers_count: int = 3):
    for _ in range(answers_count):
        create_answer_without_question()

    response = api_client.get(ANSWERS_PREFIX)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()

    assert isinstance(response_data, list), response_data
    assert len(response_data) == answers_count, response_data
    for answer_data in response_data:
        assert_valid_response(answer_data)

# def test_update_answer(api_client: TestClient):
#     pass
#
#
# def test_delete_answer_with_question(api_client: TestClient):
#     pass
#
#
# def test_delete_answer_without_question(api_client: TestClient):
#     pass
