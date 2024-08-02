import logging

from sqlmodel import Session
from typing_extensions import override

from domuwa.models.question import Question, QuestionCreate, QuestionUpdate
from domuwa.services.common_services import CommonServices

logger = logging.getLogger(__name__)


class QuestionServices(CommonServices[QuestionCreate, QuestionUpdate, Question]):
    def __init__(self) -> None:
        super().__init__(Question, logging.getLogger(__name__))

    @override
    async def update(
        self,
        model: Question,
        model_update: QuestionUpdate,
        session: Session,
    ):
        update_data = model_update.model_dump(exclude_unset=True)
        model_data = model.model_dump(exclude={"id"}) | update_data
        updated_model = Question(**model_data)

        updated_model.prev_version = model
        model.next_versions.append(updated_model)

        answers = model.answers
        if answers:
            updated_model.answers = answers

        session.add(updated_model)
        session.add(model)
        session.commit()
        session.refresh(updated_model)
        return updated_model

    @override
    async def delete(self, model: Question, session: Session):
        model.deleted = True

        for answer in model.answers:
            answer.deleted = True
            session.add(answer)

        session.add(model)
        session.commit()
        self.logger.debug("marked %s(%d) as deleted", Question.__name__, model.id)
