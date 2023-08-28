from enum import Enum

from db import crud
from db.models.game import Game
from db.models.player import Player


class EgoCategory(Enum):
    SFW = "SFW"
    NSFW = "NSFW"
    MIXED = "Mixed"


def parse_ego_category(category: str) -> EgoCategory:
    return EgoCategory[category]


class EgoGame(Game):
    def __init__(self, category: str):
        super().__init__("Ego")
        self.category = parse_ego_category(category)
        self.players: list[Player] = []

    def start(self):
        questions = crud.get_questions_for_game(self.name, self.category.value)
        available_questions = questions.copy()

    def end(self):
        for player in self.players:
            player.set_game_id(None)
            player.save()
