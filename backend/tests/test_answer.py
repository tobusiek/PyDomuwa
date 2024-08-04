from typing import Any

import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from domuwa.models.answer import Answer
from domuwa.services.answers_services import AnswerServices
from tests.common_tc import CommonTestCase
from tests.factories import (
    AnswerFactory,
    GameTypeFactory,
    PlayerFactory,
    QnACategoryFactory,
    QuestionFactory,
)


class TestAnswer(CommonTestCase[Answer]):
    path = "/api/answers/"
    services = AnswerServices()

    def assert_valid_response(self, response_data: dict[str, Any]):
        assert "id" in response_data, response_data
        assert "text" in response_data, response_data
        assert "excluded" in response_data, response_data
        assert "author" in response_data, response_data
        assert "game_type" in response_data, response_data
        assert "game_category" in response_data, response_data

    # noinspection DuplicatedCode
    def assert_valid_response_values(
        self, response_data: dict, model: Answer,
    ) -> None:
        assert response_data["id"] == model.id
        assert response_data["text"] == model.text
        assert response_data["excluded"] == model.excluded
        assert response_data["author"]["id"] == model.author.id  # type: ignore
        assert response_data["game_type"]["id"] == model.game_type.id  # type: ignore
        assert response_data["game_category"]["id"] == model.game_category.id  # type: ignore

    async def assert_valid_delete(self, model_id: int, db_session: Session) -> None:
        answer = await self.services.get_by_id(model_id, db_session)
        assert answer is not None
        assert answer.deleted

    def build_model(self):
        author = PlayerFactory.create()
        game_type = GameTypeFactory.create()
        game_category = QnACategoryFactory.create()
        return AnswerFactory.build(
            author_id=author.id,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
        )

    # noinspection DuplicatedCode
    @staticmethod
    def build_model_with_question() -> Answer:
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

    def create_model(self) -> Answer:
        author = PlayerFactory.create()
        game_type = GameTypeFactory.create()
        game_category = QnACategoryFactory.create()
        return AnswerFactory.create(
            author_id=author.id,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
        )

    # noinspection DuplicatedCode
    @staticmethod
    def create_model_with_question() -> Answer:
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

    # noinspection DuplicatedCode
    def test_update(self, api_client: TestClient):
        import warnings

        warnings.filterwarnings("ignore", module="sqlmodel.orm.session")

        answer = self.create_model()
        new_text = 'new text'

        response = api_client.patch(
            f"{self.path}{answer.id}",
            json={"text": new_text},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)

        assert response_data["id"] >= answer.id, response_data

        assert response_data["text"] != answer.text, response_data
        assert response_data["text"] == new_text, response_data

        assert response_data["excluded"] == answer.excluded, response_data

        # TODO: after auth
        # assert response_data["author"]["id"] != answer.author.id
        # assert response_data["author"]["name"] == answer.author.name

        assert response_data["game_type"]["id"] == answer.game_type.id, response_data  # type: ignore
        assert response_data["game_type"]["name"] == answer.game_type.name  # type: ignore

        assert (
                response_data["game_category"]["id"] == answer.game_category.id  # type: ignore
        ), response_data
        assert response_data["game_category"]["name"] == answer.game_category.name  # type: ignore

    # noinspection DuplicatedCode
    @pytest.mark.asyncio
    async def test_create_answer_with_question(self, api_client: TestClient, db_session: Session):
        answer = self.build_model_with_question()

        response = api_client.post(self.path, json=answer.model_dump())
        assert response.status_code == status.HTTP_201_CREATED, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)

        response = api_client.get(f"{self.path}{response_data['id']}")
        assert response.status_code == status.HTTP_200_OK, response.text
        answer_response_data = response.json()
        self.assert_valid_response(answer_response_data)

        db_answer = await self.services.get_by_id(response_data["id"], db_session)
        assert db_answer is not None

        question = db_answer.question
        assert question is not None
        answer.id = response_data["id"]
        assert answer == question.answers[0], question.answers

    @pytest.mark.asyncio
    async def test_delete_answer_with_question(self, api_client: TestClient, db_session: Session):
        answer = self.create_model_with_question()
        answer_id = answer.id
        assert answer_id is not None

        response = api_client.delete(f"{self.path}{answer_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

        response = api_client.get(f"{self.path}{answer_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

        db_answer = await self.services.get_by_id(answer_id, db_session)
        assert db_answer is not None

        question = db_answer.question
        assert question is not None
        assert not question.deleted
