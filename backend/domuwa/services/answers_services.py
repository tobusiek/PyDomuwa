import logging

from sqlmodel import Session
from typing_extensions import override

from domuwa.models.answer import Answer, AnswerCreate, AnswerUpdate
from domuwa.services.common_services import CommonServices


class AnswerServices(CommonServices[AnswerCreate, AnswerUpdate, Answer]):
    def __init__(self) -> None:
        super().__init__(Answer, logging.getLogger(__name__))

    @override
    async def update(
        self,
        model: Answer,
        model_update: AnswerUpdate,
        session: Session,
    ):
        update_data = model_update.model_dump(exclude_unset=True)
        model_data = model.model_dump(exclude={"id"}) | update_data
        updated_model = Answer(**model_data)

        updated_model.prev_version = model
        model.next_versions.append(updated_model)

        question = model.question
        if question is not None:
            question.answers.remove(model)
            question.answers.append(updated_model)
            session.add(question)

        session.add(updated_model)
        session.add(model)
        session.commit()
        session.refresh(updated_model)
        return updated_model

    @override
    async def delete(self, model: Answer, session: Session):
        model.deleted = True
        session.add(model)
        session.commit()
        self.logger.debug("marked %s(id=%d) as deleted", Answer.__name__, model.id)  # type: ignore
