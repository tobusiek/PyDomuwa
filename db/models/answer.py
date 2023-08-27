import logging
from sqlite3 import OperationalError
from typing import Optional

from db.database import execute_query, execute_query_and_commit
from db.models.db_model import DbModel

logger = logging.getLogger("db_connector")


class Answer(DbModel):
    table_name = "answer"

    def __init__(self, text: str, question_id: int, answer_id: int = 0, points: float = None):
        super().__init__(answer_id)
        self.text = text
        self.points = points
        self.question_id = question_id

    def edit_text(self, text: str) -> None:
        self.text = text
        edit_text = f"""
        UPDATE {self.table_name} SET text = ? WHERE id = ?;
        """
        query_params = (self.text, self.id)
        execute_query_and_commit(edit_text, query_params)

    def edit_points(self, points: float) -> None:
        self.points = points
        edit_points = f"""
        UPDATE {self.table_name} SET points = ? WHERE id = ?;
        """
        query_params = (self.points, self.id)
        execute_query_and_commit(edit_points, query_params)

    def delete(self) -> None:
        delete = f"""
        DELETE FROM {self.table_name} WHERE id = ?;
        """
        query_params = (self.id,)
        execute_query_and_commit(delete, query_params)

    @classmethod
    def create_table(cls) -> None:
        create_answer_table = f"""
        CREATE TABLE IF NOT EXISTS {cls.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            text TEXT NOT NULL,
            points REAL
        );
        """
        execute_query_and_commit(create_answer_table)

    @classmethod
    def create_foreign_key(cls, question_table_name: str) -> None:
        create_foreign_key = f"""
        ALTER TABLE {cls.table_name} ADD COLUMN question_id INTEGER REFERENCES {question_table_name}(id);
        """
        try:
            execute_query_and_commit(create_foreign_key)
        except OperationalError:
            logger.debug("Answer.question_id already exists")

    def save(self) -> None:
        insert_answer = f"""
        INSERT INTO {self.table_name} (text, points, question_id) VALUES (?, ?, ?);
        """
        query_params = (self.text, self.points, self.question_id)
        execute_query_and_commit(insert_answer, query_params)

    @classmethod
    def get_all(cls) -> list["Answer"]:
        select_answers = f"""
        SELECT text, question_id, id, points FROM {cls.table_name};
        """
        answers_data = execute_query(select_answers).fetchall()
        answers = [Answer(**answer_data) for answer_data in answers_data]
        return answers

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

    @classmethod
    def get_by_question_id(cls, question_id: int) -> list["Answer"]:
        select_answers = f"""
        SELECT text, question_id, id, points FROM {cls.table_name} WHERE question_id = ?;
        """
        query_params = (question_id,)
        answers_data = execute_query(select_answers, query_params).fetchall()
        answers = [Answer(**answer_data) for answer_data in answers_data]
        return answers
