import logging

from sqlmodel import Session, select

from domuwa.models.qna_category import QnACategory, QnACategoryCreate, QnACategoryUpdate
from domuwa.services.common_services import CommonServices


class QnACategoryServices(
    CommonServices[QnACategoryCreate, QnACategoryUpdate, QnACategory]
):
    def __init__(self) -> None:
        super().__init__(QnACategory, logging.getLogger(__name__))

    async def create(self, model: QnACategoryCreate, session: Session):
        db_qna_category = session.exec(select(QnACategory).where(QnACategory.name == model.name)).first()
        if db_qna_category is not None:
            self.logger.warning("QnACategory(name=%s) already exists", model.name)
            return None
        return await super().create(model, session)

    async def update(
        self,
        model: QnACategory,
        model_update: QnACategoryUpdate,
        session: Session,
    ):
        db_qna_category = session.exec(select(QnACategory).where(QnACategory.name == model_update.name)).first()
        if db_qna_category is not None:
            self.logger.warning("QnACategory(name=%s) already exists", model.name)
            return None
        return await super().update(model, model_update, session)
