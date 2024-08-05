import logging

from domuwa.models.qna_category import QnACategory, QnACategoryCreate, QnACategoryUpdate
from domuwa.services.common_services import CommonServices


class QnACategoryServices(
    CommonServices[QnACategoryCreate, QnACategoryUpdate, QnACategory]
):
    def __init__(self) -> None:
        super().__init__(QnACategory, logging.getLogger(__name__))
