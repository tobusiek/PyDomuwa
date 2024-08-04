import logging

from sqlmodel import Session, select

from domuwa.models.player import Player, PlayerCreate, PlayerUpdate
from domuwa.services.common_services import CommonServices


class PlayerServices(CommonServices[PlayerCreate, PlayerUpdate, Player]):
    def __init__(self) -> None:
        super().__init__(Player, logging.getLogger(__name__))

    async def create(self, model: PlayerCreate, session: Session):
        db_player = session.exec(
            select(Player).where(Player.name == model.name)
        ).first()
        if db_player is not None:
            self.logger.warning("Player(name=%s) already exists.", model.name)
            return None
        return await super().create(model, session)
