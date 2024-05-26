import logging

from fastapi import APIRouter, Depends
from sqlmodel import Session

from domuwa.database import get_db_session
from domuwa.models.question import QuestionWithAnswersRead
from domuwa.services import questions_services as services

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/questions", tags=["Question"])


@router.get("/{question_id}", response_model=QuestionWithAnswersRead)
async def get_question_by_id(
    question_id: int,
    db_sess: Session = Depends(get_db_session),
):
    logger.debug("received Question(id=%d) to get", question_id)
    return await services.get_question_by_id(question_id, db_sess)
