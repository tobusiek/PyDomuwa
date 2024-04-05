from pydantic import BaseModel

from domuwa.models.db_models import QnACategoryChoices


class QnACategoryBase(BaseModel):
    name: QnACategoryChoices


class QnACategoryCreate(QnACategoryBase):
    pass


class QnACategoryRead(QnACategoryBase):
    id: int


class QnACategoryUpdate(QnACategoryBase):
    pass
