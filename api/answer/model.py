from sqlalchemy import Column, Integer, String, Float, ForeignKey
from sqlalchemy.orm import Mapped, relationship

from api.database import Base
from api.question.model import Question


class Answer(Base):
    __tablename__ = "answer"

    id: Mapped[int] = Column(Integer, primary_key=True, autoincrement=True)
    text: Mapped[str] = Column(String, nullable=False)
    points: Mapped[float] = Column(Float, nullable=True, default=0.0)
    question_id: Mapped[int] = Column(Integer, ForeignKey("question", column="question.id", ondelete="CASCADE"))
    question: Mapped[Question] = relationship("Question", back_populates="answers")
