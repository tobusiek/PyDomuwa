from enum import Enum

from db.models.game import Game


class EgoCategory(Enum):
    SFW = "SFW"
    NSFW = "NSFW"
    MIXED = "MIXED"


def parse_ego_category(category: str) -> EgoCategory:
    return EgoCategory[category]


class EgoGame(Game):
    def __init__(self, category: str):
        super().__init__("Ego")
        self.category = parse_ego_category(category)

    def start_game(self):
        raise NotImplemented()
