import logging

from domuwa.models.player import Player, PlayerCreate, PlayerUpdate
from domuwa.services.common_services import CommonServices


class PlayerServices(CommonServices[PlayerCreate, PlayerUpdate, Player]):
    def __init__(self) -> None:
        super().__init__(Player, logging.getLogger(__name__))
