from sqlmodel import SQLModel

from domuwa.models.answer import *  # noqa: F403
from domuwa.models.game_category import *  # noqa: F403
from domuwa.models.game_room import *  # noqa: F403
from domuwa.models.game_type import *  # noqa: F403
from domuwa.models.links import *  # noqa: F403
from domuwa.models.player import *  # noqa: F403
from domuwa.models.player_score import *  # noqa: F403
from domuwa.models.qna_category import *  # noqa: F403
from domuwa.models.question import *  # noqa: F403
from domuwa.models.ranking import *  # noqa: F403


def get_subclasses(cls: type[SQLModel]):
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass


models = get_subclasses(SQLModel)
for cls in models:
    cls.model_rebuild()
