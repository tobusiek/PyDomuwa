from typing import TYPE_CHECKING, Optional

from sqlmodel import Field, Relationship, SQLModel

from domuwa.models.links import GameRoomQuestionsLink

if TYPE_CHECKING:
    from domuwa.models.answer import Answer
    from domuwa.models.game_room import GameRoom
    from domuwa.models.game_type import GameType
    from domuwa.models.player import Player
    from domuwa.models.qna_category import QnACategory


class Question(SQLModel, table=True):
    __tablename__ = "question"  # type: ignore

    id: Optional[int] = Field(None, primary_key=True)
    text: str = Field(min_length=3, max_length=150)
    excluded: bool = Field(False, index=True)

    author_id: Optional[str] = Field(None, foreign_key="player.id")
    author: Optional["Player"] = Relationship(back_populates="questions")

    game_type_id: Optional[int] = Field(None, foreign_key="game_type.id")
    game_type: Optional["GameType"] = Relationship(back_populates="questions")

    game_category_id: Optional[int] = Field(None, foreign_key="qna_category.id")
    game_category: Optional["QnACategory"] = Relationship(back_populates="questions")

    answers: list["Answer"] = Relationship(back_populates="question")

    game_rooms: list["GameRoom"] = Relationship(
        back_populates="questions",
        link_model=GameRoomQuestionsLink,
    )
