from typing import Optional

from db.database import execute_query_and_commit, execute_query
from db.models.db_model import DbModel


class Game(DbModel):
    table_name = "game"

    def __init__(self, name: str, game_id: int = None):
        super().__init__(game_id)
        self.name = name

    @classmethod
    def create_table(cls) -> None:
        create_game_table = f"""
            CREATE TABLE IF NOT EXISTS {cls.table_name} (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL
            );
            """
        execute_query_and_commit(create_game_table)

    def save(self) -> None:
        insert_game = f"""
        INSERT INTO {self.table_name} (name) VALUES (?);
        """
        game_data = (self.name,)
        execute_query_and_commit(insert_game, game_data)

    @classmethod
    def get_all(cls) -> list["Game"]:
        select_games = f"""
        SELECT id, name FROM {cls.table_name};
        """
        games_data = execute_query(select_games).fetchall()
        games = [Game(name, game_id) for game_id, name in games_data]
        return games

    @classmethod
    def get_by_id(cls, model_id: int) -> Optional["Game"]:
        select_game = f"""
        SELECT name, id FROM {cls.table_name} WHERE id = ?;
        """
        query_params = (model_id,)
        game_data = execute_query(select_game, query_params).fetchone()
        if not game_data:
            return None
        return Game(**game_data)
