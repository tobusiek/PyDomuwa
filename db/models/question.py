from typing import Optional

from db.database import execute_query
from db.models.db_model import DbModel


class Question(DbModel):
    table_name = "question"

    def __init__(self, game_name: str, text: str, question_id: int = 0, correct_answer_id: int = None):
        super().__init__(question_id)
        self.game_name = game_name
        self.text = text
        self.correct_answer_id = correct_answer_id

    @classmethod
    def create_table(cls) -> None:
        # TODO: make sql stmt
        pass

    def save(self) -> None:
        # TODO: make sql stmt
        pass

    @classmethod
    def get_all(cls) -> list["Question"]:
        # TODO: make sql stmt
        pass

    @classmethod
    def get_by_id(cls, model_id: int) -> Optional["Question"]:
        select_question = f"""
        SELECT game_name, text, id, correct_answer_id FROM {cls.table_name} WHERE id = ?;
        """
        query_params = (model_id,)
        question_data = execute_query(select_question, query_params).fetchone()
        if not question_data:
            return None
        return Question(**question_data)
