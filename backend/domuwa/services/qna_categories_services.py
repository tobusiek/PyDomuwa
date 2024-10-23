import logging

from domuwa.models.qna_category import QnACategory, QnACategoryCreate, QnACategoryUpdate
from domuwa.services.common_services import CommonServices


class QnACategoryServices(
    CommonServices[QnACategoryCreate, QnACategoryUpdate, QnACategory]
):
    db_model_type = QnACategory
    logger = logging.getLogger(__name__)
