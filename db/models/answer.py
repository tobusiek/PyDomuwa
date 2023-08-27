from typing import Optional

from db.database import execute_query
from db.models.db_model import DbModel


class Answer(DbModel):
    table_name = "answer"

    def __init__(self, text: str, question_id: int, answer_id: int = 0, points: float = None):
        super().__init__(answer_id)
        self.text = text
        self.points = points
        self.question_id = question_id

    @classmethod
    def create_table(cls) -> None:
        # TODO: make sql stmt
        pass

    def save(self) -> None:
        # TODO: make sql stmt
        pass

    @classmethod
    def get_all(cls) -> list["Answer"]:
        # TODO: make sql stmt
        pass

    @classmethod
    def get_by_id(cls, model_id: int) -> Optional["Answer"]:
        select_answer = f"""
        SELECT text, question_id, id, points FROM {cls.table_name} WHERE id = ?;
        """
        query_params = (model_id,)
        answer_data = execute_query(select_answer, query_params).fetchone()
        if not answer_data:
            return None
        return Answer(**answer_data)
