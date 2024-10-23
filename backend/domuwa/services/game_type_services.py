import logging

from domuwa.models.game_type import GameType, GameTypeCreate, GameTypeUpdate
from domuwa.services.common_services import CommonServices


class GameTypeServices(CommonServices[GameTypeCreate, GameTypeUpdate, GameType]):
    db_model_type = GameType
    logger = logging.getLogger(__name__)
