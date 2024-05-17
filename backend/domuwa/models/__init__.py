from sqlmodel import SQLModel

from domuwa.models.answer import *
from domuwa.models.game_category import *
from domuwa.models.game_room import *
from domuwa.models.game_type import *
from domuwa.models.links import *
from domuwa.models.player import *
from domuwa.models.player_score import *
from domuwa.models.qna_category import *
from domuwa.models.question import *
from domuwa.models.ranking import *


def get_subclasses(cls: type[SQLModel]):
    for subclass in cls.__subclasses__():
        yield from get_subclasses(subclass)
        yield subclass


models = get_subclasses(SQLModel)
for cls in models:
    cls.model_rebuild()
