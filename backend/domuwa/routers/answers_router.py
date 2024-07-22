import logging

from fastapi import APIRouter, Depends, status
from fastapi_class import Method, View, endpoint
from sqlmodel import Session

from domuwa.database import get_db_session
from domuwa.models.answer import (
    Answer,
    AnswerCreate,
    AnswerRead,
    AnswerUpdate,
)
from domuwa.routers.generics import (
    CreateRouter,
    DeleteRouter,
    RetrieveRouter,
    UpdateRouter,
)
from domuwa.services.answers_services import AnswerServices

router = APIRouter(prefix="/answers", tags=["Answer"])


@View(router)
class AnswerRouter(
    CreateRouter[AnswerCreate, Answer],
    RetrieveRouter[Answer],
    UpdateRouter[AnswerUpdate, Answer],
    DeleteRouter[Answer],
):
    services = AnswerServices()
    logger = logging.getLogger(__name__)
    db_model_type_name = Answer.__name__

    RESPONSE_MODEL_ATTRIBUTE_NAME = {
        "create_answer": AnswerRead,
        "get_answer_by_id": AnswerRead,
        "get_all_answers": list[AnswerRead],
        "update_answer": AnswerRead,
    }

    @endpoint(Method.POST, status_code=status.HTTP_201_CREATED)
    async def create(
        self,
        answer_create: AnswerCreate,
        session: Session = Depends(get_db_session),
    ):
        return await self._post(answer_create, session)

    @endpoint(Method.GET, path="{answer_id}")
    async def get_by_id(
        self,
        answer_id: int,
        session: Session = Depends(get_db_session),
    ):
        return await self._get_by_id(answer_id, session)

    @endpoint(Method.GET)
    async def get_all(self, session: Session = Depends(get_db_session)):
        return await self._get_all(session)

    @endpoint(Method.PATCH, path="{answer_id}")
    async def update(
        self,
        answer_id: int,
        answer_update: AnswerUpdate,
        session: Session = Depends(get_db_session),
    ):
        return await self._patch(answer_id, answer_update, session)

    @endpoint(Method.DELETE, path="{answer_id}", status_code=status.HTTP_204_NO_CONTENT)
    async def delete(
        self,
        answer_id: int,
        session: Session = Depends(get_db_session),
    ):
        return await self._delete(answer_id, session)
