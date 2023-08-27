from enum import Enum

from db.models.game import Game


class EgoCategory(Enum):
    SFW = "SFW"
    NSFW = "NSFW"
    MIXED = "MIXED"


def parse(category: str) -> EgoCategory:
    return EgoCategory[category]


class EgoGame(Game):
    def __init__(self, name: str, category: EgoCategory):
        super().__init__(name)
        self.name = name
        self.category = category

    def start_game(self):
        raise NotImplemented()
