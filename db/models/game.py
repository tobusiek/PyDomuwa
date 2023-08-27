import logging
from sqlite3 import OperationalError
from typing import Optional

from db.database import execute_query_and_commit, execute_query
from db.models.db_model import DbModel

logger = logging.getLogger("db_connector")


class Game(DbModel):
    table_name = "game"

    def __init__(self, name: str, game_id: int = None, category: str = None, rounds: int = None, cur_round: int = 0):
        super().__init__(game_id)
        self.name = name
        self.category = category
        self.rounds = rounds
        self.cur_round = cur_round

    @classmethod
    def create_table(cls) -> None:
        create_game_table = f"""
        CREATE TABLE IF NOT EXISTS {cls.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            category TEXT,
            rounds INTEGER,
            cur_round INTEGER
        );
        """
        execute_query_and_commit(create_game_table)

    def save(self) -> None:
        insert_game = f"""
        INSERT INTO {self.table_name} (name, category, rounds, cur_round) VALUES (?, ?, ?, ?);
        """
        query_params = (self.name, self.category, self.rounds, self.cur_round)
        execute_query_and_commit(insert_game, query_params)

    def update_cur_round(self) -> None:
        self.cur_round += 1
        update_cur_round = f"""
        UPDATE {self.table_name} SET cur_round = ? WHERE id = ?;
        """
        query_params = (self.cur_round, self.id)
        execute_query_and_commit(update_cur_round, query_params)

    def delete(self) -> None:
        delete_game = f"""
        DELETE FROM {self.table_name} WHERE id = ?;
        """
        query_params = (self.id,)
        execute_query_and_commit(delete_game, query_params)

    @classmethod
    def delete_all(cls) -> None:
        delete_games = f"""
        DELETE FROM {cls.table_name};
        """
        try:
            execute_query_and_commit(delete_games)
        except OperationalError:
            logger.debug("No games to delete")

    @classmethod
    def get_all(cls) -> list["Game"]:
        select_games = f"""
        SELECT name, id, category, rounds, cur_round FROM {cls.table_name};
        """
        games_data: list[tuple] = execute_query(select_games).fetchall()
        games = [Game(*game_data) for game_data in games_data]
        return games

    @classmethod
    def get_by_id(cls, model_id: int) -> Optional["Game"]:
        select_game = f"""
        SELECT name, id, category, rounds, cur_round FROM {cls.table_name} WHERE id = ?;
        """
        query_params = (model_id,)
        game_data = execute_query(select_game, query_params).fetchone()
        if not game_data:
            return None
        return Game(*game_data)
