from sqlalchemy import Integer, Column, String, ForeignKey
from sqlalchemy.orm import relationship

from db.database import Base


class Answer(Base):
    __tablename__ = 'answers'
    id = Column(Integer, primary_key=True, index=True)
    text = Column(String, nullable=False)
    points = Column(Integer, nullable=True)
    question_id = Column(Integer, ForeignKey('question.id'), nullable=False)
    question = relationship('Question', back_populates='answers')
