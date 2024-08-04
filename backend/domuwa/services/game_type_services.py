import logging

from domuwa.models.game_type import GameType, GameTypeCreate, GameTypeUpdate
from domuwa.services.common_services import CommonServices


class GameTypeServices(CommonServices[GameTypeCreate, GameTypeUpdate, GameType]):
    def __init__(self) -> None:
        super().__init__(GameType, logging.getLogger(__name__))
