import logging

from sqlmodel import Session, select

from domuwa.models.game_type import GameType, GameTypeCreate, GameTypeUpdate
from domuwa.services.common_services import CommonServices


class GameTypeServices(CommonServices[GameTypeCreate, GameTypeUpdate, GameType]):
    def __init__(self) -> None:
        super().__init__(GameType, logging.getLogger(__name__))

    async def create(self, model: GameTypeCreate, session: Session):
        db_game_type = session.exec(
            select(GameType).where(GameType.name == model.name)
        ).first()
        if db_game_type is not None:
            self.logger.warning("GameType(name=%s) already exists.", model.name)
            return None
        return await super().create(model, session)

    # noinspection DuplicatedCode
    async def update(self, model: GameType, model_update: GameTypeUpdate, session: Session):
        db_game_type = session.exec(
            select(GameType).where(GameType.name == model_update.name)
        ).first()
        if db_game_type is not None:
            self.logger.warning("GameType(name=%s) already exists.", model.name)
            return None
        return await super().update(model, model_update, session)
