from typing import Any

from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from domuwa import database as db
from domuwa.models.question import Question
from domuwa.tests.factories import (
    GameTypeFactory,
    PlayerFactory,
    QnACategoryFactory,
    QuestionFactory,
)

QUESTIONS_PREFIX = "/api/questions/"


def dump_question(question: Question):
    return question.model_dump()


def assert_valid_response(response_data: dict[str, Any]):
    assert "id" in response_data, response_data
    assert "text" in response_data, response_data
    assert "excluded" in response_data, response_data
    assert "author" in response_data, response_data
    assert "game_type" in response_data, response_data
    assert "game_category" in response_data, response_data


def build_question():
    author = PlayerFactory.create()
    game_type = GameTypeFactory.create()
    game_category = QnACategoryFactory.create()
    return QuestionFactory.build(
        author_id=author.id,
        game_type_id=game_type.id,
        game_category_id=game_category.id,
    )


def create_question():
    author = PlayerFactory.create()
    game_type = GameTypeFactory.create()
    game_category = QnACategoryFactory.create()
    return QuestionFactory.create(
        author_id=author.id,
        game_type_id=game_type.id,
        game_category_id=game_category.id,
    )


def test_create_question(api_client: TestClient):
    question = build_question()

    response = api_client.post(QUESTIONS_PREFIX, json=dump_question(question))
    assert response.status_code == status.HTTP_201_CREATED, response.text
    response_data = response.json()
    assert_valid_response(response_data)

    response = api_client.get(f"{QUESTIONS_PREFIX}{response_data['id']}")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert_valid_response(response_data)


def test_get_question_by_id(api_client: TestClient):
    question = create_question()

    response = api_client.get(f"{QUESTIONS_PREFIX}{question.id}")
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()
    assert_valid_response(response_data)

    assert response_data["id"] == question.id
    assert response_data["text"] == question.text
    assert response_data["excluded"] == question.excluded
    assert response_data["author"]["id"] == question.author.id
    assert response_data["game_type"]["id"] == question.game_type.id
    assert response_data["game_category"]["id"] == question.game_category.id


def test_get_all_answers(api_client: TestClient, questions_count: int = 3):
    for _ in range(questions_count):
        create_question()

    response = api_client.get(QUESTIONS_PREFIX)
    assert response.status_code == status.HTTP_200_OK, response.text
    response_data = response.json()

    assert isinstance(response_data, list), response_data
    assert len(response_data) == questions_count, response_data
    for question_data in response_data:
        assert_valid_response(question_data)


def test_update_question_without_answers(api_client: TestClient):
    pass


def test_update_question_with_answers(api_client: TestClient):
    pass


def test_delete_question_without_answers(api_client: TestClient):
    pass


def test_delete_question_with_answers(api_client: TestClient, db_session: Session):
    question = create_question()

    response = api_client.delete(f"{QUESTIONS_PREFIX}{question.id}")
    assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

    # TODO: finish
    db.get(question.id, db_session)
