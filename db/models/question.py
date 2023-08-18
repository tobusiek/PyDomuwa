from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Question(Base):
    __tablename__ = "questions"
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    answers = relationship("Answer", back_populates="questions")
    correct_answer_id = Column(Integer)
