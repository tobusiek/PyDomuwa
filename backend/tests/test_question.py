import pytest
from fastapi import status
from fastapi.testclient import TestClient
from sqlmodel import Session

from domuwa.models.question import Question
from domuwa.services.questions_services import QuestionServices
from tests.common_tc import CommonTestCase
from tests.factories import (
    AnswerFactory,
    GameTypeFactory,
    PlayerFactory,
    QnACategoryFactory,
    QuestionFactory,
)


class TestQuestion(CommonTestCase[Question]):
    path = "/api/questions/"
    services = QuestionServices()

    def assert_valid_response(self, response_data: dict) -> None:
        assert "id" in response_data, response_data
        assert "text" in response_data, response_data
        assert "excluded" in response_data, response_data
        assert "author" in response_data, response_data
        assert "game_type" in response_data, response_data
        assert "game_category" in response_data, response_data

    # noinspection DuplicatedCode
    def assert_valid_response_values(self, response_data: dict, model: Question) -> None:
        assert response_data["id"] == model.id
        assert response_data["text"] == model.text
        assert response_data["excluded"] == model.excluded
        assert response_data["author"]["id"] == model.author.id  # type: ignore
        assert response_data["game_type"]["id"] == model.game_type.id  # type: ignore
        assert response_data["game_category"]["id"] == model.game_category.id  # type: ignore

    async def assert_valid_delete(self, model_id: int, db_session: Session) -> None:
        question = await self.services.get_by_id(model_id, db_session)
        assert question is not None
        assert question.deleted
        for answer in question.answers:
            assert answer.deleted

    def build_model(self) -> Question:
        author = PlayerFactory.create()
        game_type = GameTypeFactory.create()
        game_category = QnACategoryFactory.create()
        return QuestionFactory.build(
            author_id=author.id,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
        )

    def create_model(self) -> Question:
        author = PlayerFactory.create()
        game_type = GameTypeFactory.create()
        game_category = QnACategoryFactory.create()
        return QuestionFactory.create(
            author_id=author.id,
            game_type_id=game_type.id,
            game_category_id=game_category.id,
        )

    # noinspection DuplicatedCode
    def test_update(self, api_client: TestClient):
        import warnings

        warnings.filterwarnings("ignore", module="sqlmodel.orm.session")

        question = self.create_model()
        new_text = "new text"

        response = api_client.patch(
            f"{self.path}{question.id}",
            json={"text": new_text},
        )
        assert response.status_code == status.HTTP_200_OK, response.text
        response_data = response.json()
        self.assert_valid_response(response_data)

        assert response_data["id"] >= question.id, response_data

        assert response_data["text"] != question.text, response_data
        assert response_data["text"] == new_text, response_data

        assert response_data["excluded"] == question.excluded, response_data

        # TODO: after auth
        # assert response_data["author"]["id"] != question.author.id
        # assert response_data["author"]["id"] == new_author.id

        assert response_data["game_type"]["id"] == question.game_type.id, response_data  # type: ignore
        assert response_data["game_type"]["name"] == question.game_type.name  # type: ignore

        assert (
                response_data["game_category"]["id"] == question.game_category.id  # type: ignore
        ), response_data
        assert response_data["game_category"]["name"] == question.game_category.name  # type: ignore

        assert not response_data["answers"], response_data

    # noinspection DuplicatedCode
    @pytest.mark.asyncio
    async def test_delete_with_answers(self, api_client: TestClient, db_session: Session):
        model = self.create_model()
        model_id = model.id
        assert model_id is not None

        AnswerFactory.create_batch(2, question_id=model_id)

        response = api_client.delete(f"{self.path}{model_id}")
        assert response.status_code == status.HTTP_204_NO_CONTENT, response.text

        response = api_client.get(f"{self.path}{model_id}")
        assert response.status_code == status.HTTP_404_NOT_FOUND, response.text

        await self.assert_valid_delete(model_id, db_session)
