from sqlalchemy import Column, Double, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Player(Base):
    __tablename__ = "players"
    id = Column(name='id', type_=Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    score = Column(Double, nullable=False)
    rankings = relationship("Ranking", back_populates="player")
