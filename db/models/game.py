from enum import Enum

from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from db.database import Base


class Game(Base):
    __tablename__ = "games"
    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    players = relationship("Player", secondary="game_players")
    questions = relationship("Question")


def parse(category: str) -> 'EgoCategory':
    return EgoCategory[category]


class EgoCategory(Enum):
    SFW = 'SFW'
    NSFW = 'NSFW'
    MIXED = 'MIXED'


class EgoGame(Game):
    def __init__(self, name: str, category: EgoCategory):
        self.name = name
        self.category = category
