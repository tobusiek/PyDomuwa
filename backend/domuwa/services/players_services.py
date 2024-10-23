import logging

from domuwa.models.player import Player, PlayerCreate, PlayerUpdate
from domuwa.services.common_services import CommonServices


class PlayerServices(CommonServices[PlayerCreate, PlayerUpdate, Player]):
    db_model_type = Player
    logger = logging.getLogger(__name__)
