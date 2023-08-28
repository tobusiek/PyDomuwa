import logging
from sqlite3 import OperationalError
from typing import Optional

from db.database import execute_query, execute_query_and_commit
from db.models.db_model import DbModel

logger = logging.getLogger("db_connector")


class Question(DbModel):
    table_name = "question"

    def __init__(self, game_name: str, category: str, text: str, question_id: int = 0, correct_answer_id: int = None):
        super().__init__(question_id)
        self.game_name = game_name
        self.category = category
        self.text = text
        self.correct_answer_id = correct_answer_id

    @classmethod
    def create_table(cls) -> None:
        create_question_table = f"""
        CREATE TABLE IF NOT EXISTS {cls.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            game_name TEXT NOT NULL,
            category TEXT NOT NULL,
            text TEXT NOT NULL
        );
        """
        execute_query_and_commit(create_question_table)

    @classmethod
    def create_index(cls) -> None:
        create_index = f"""
        CREATE INDEX IF NOT EXISTS {cls.table_name}_game_type_IDX
        ON {cls.table_name} (game_name, category);
        """
        execute_query_and_commit(create_index)

    @classmethod
    def create_foreign_key(cls, answer_table_name: str) -> None:
        create_foreign_key = f"""
        ALTER TABLE {cls.table_name} ADD COLUMN correct_answer_id INTEGER REFERENCES {answer_table_name}(id);
        """
        try:
            execute_query_and_commit(create_foreign_key)
        except OperationalError:
            logger.debug("Question.correct_answer_id already exists")

    def save(self) -> None:
        insert_question = f"""
        INSERT INTO {self.table_name} (game_name, category, text, correct_answer_id) VALUES (?, ?, ?, ?);
        """
        query_params = (self.game_name, self.category, self.text, self.correct_answer_id)
        execute_query_and_commit(insert_question, query_params)

    def delete(self) -> None:
        delete_question = f"""
        DELETE FROM {self.table_name} WHERE id = ?;
        """
        query_params = (self.id,)
        execute_query_and_commit(delete_question, query_params)

    @classmethod
    def get_all(cls) -> list["Question"]:
        select_questions = f"""
        SELECT game_name, category, text, id, correct_answer_id FROM {cls.table_name};
        """
        questions_data = execute_query(select_questions).fetchall()
        questions = [Question(*question_data) for question_data in questions_data]
        return questions

    @classmethod
    def get_by_id(cls, model_id: int) -> Optional["Question"]:
        select_question = f"""
        SELECT game_name, category, text, id, correct_answer_id FROM {cls.table_name} WHERE id = ?;
        """
        query_params = (model_id,)
        question_data = execute_query(select_question, query_params).fetchone()
        if not question_data:
            return None
        return Question(*question_data)

    @classmethod
    def get_by_game_type(cls, game_name: str, game_category: str) -> list["Question"]:
        select_questions = f"""
        SELECT game_name, category, text, id, correct_answer_id FROM {cls.table_name}
        WHERE game_name = ? AND category = ?;
        """
        query_params = (game_name, game_category)
        questions_data = execute_query(select_questions, query_params).fetchall()
        questions = [Question(*question_data) for question_data in questions_data]
        return questions
