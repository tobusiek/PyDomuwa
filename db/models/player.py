import logging
from sqlite3 import OperationalError
from typing import Optional

from db.database import execute_query, execute_query_and_commit
from db.models.db_model import DbModel

logger = logging.getLogger("db_connector")


class Player(DbModel):
    table_name = "player"

    def __init__(self, name: str, player_id: int = None, score: float = 0.0, game_id: int = None):
        super().__init__(player_id)
        self.name = name
        self.score = score
        self.game_id = game_id

    def update_score(self, points: float) -> None:
        self.score += points
        update_player_score = f"""
        UPDATE {self.table_name} SET score = ? WHERE id = ?;
        """
        query_params = (self.score, self.id)
        execute_query_and_commit(update_player_score, query_params)

    def clear_score(self) -> None:
        self.score = 0.0
        clear_player_score = f"""
        UPDATE {self.table_name} SET score = ? WHERE id = ?;
        """
        query_params = (self.score, self.id)
        execute_query_and_commit(clear_player_score, query_params)

    def set_game_id(self, game_id: int | None) -> None:
        self.game_id = game_id
        set_game_id = f"""
        UPDATE {self.table_name} SET game_id = ? WHERE id = ?;
        """
        query_params = (self.game_id, self.id)
        execute_query_and_commit(set_game_id, query_params)

    @classmethod
    def create_table(cls):
        create_player_table = f"""
        CREATE TABLE IF NOT EXISTS {cls.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score REAL NOT NULL
        );
        """
        execute_query_and_commit(create_player_table)

    @classmethod
    def create_index(cls) -> None:
        create_index = f"""
        CREATE INDEX IF NOT EXISTS {cls.table_name}_name_IDX
        ON {cls.table_name} (name);
        """
        execute_query_and_commit(create_index)

    @classmethod
    def create_foreign_key(cls, game_table_name: str) -> None:
        create_foreign_key = f"""
        ALTER TABLE {cls.table_name} ADD COLUMN game_id INTEGER REFERENCES {game_table_name}(id);
        """
        try:
            execute_query_and_commit(create_foreign_key)
        except OperationalError:
            logger.debug("Player.game_id already exists")

    def save(self):
        insert_player = f"""
        INSERT INTO {self.table_name} (name, score, game_id) VALUES (?, ?, ?);
        """
        query_params = (self.name, self.score, self.game_id)
        execute_query_and_commit(insert_player, query_params)

    @classmethod
    def get_all(cls) -> list["Player"]:
        select_players = f"""
        SELECT name, id, score, game_id FROM {cls.table_name};
        """
        players_data = execute_query(select_players).fetchall()
        players = [Player(*player_data) for player_data in players_data]
        return players

    @classmethod
    def get_by_id(cls, model_id: int) -> Optional["Player"]:
        select_player = f"""
        SELECT name, id, score, game_id FROM {cls.table_name} WHERE id = ?;
        """
        query_params = (model_id,)
        player_data = execute_query(select_player, query_params).fetchone()
        if not player_data:
            return None
        return Player(*player_data)

    @classmethod
    def get_by_name(cls, name: str) -> Optional["Player"]:
        select_player = f"""
        SELECT name, id, score, game_id FROM {cls.table_name} WHERE name = ?;
        """
        query_params = (name,)
        player_data = execute_query(select_player, query_params).fetchone()
        if not player_data:
            return None
        return Player(*player_data)

    @classmethod
    def get_by_game_id(cls, game_id: int) -> list["Player"]:
        select_players = f"""
        SELECT name, id, score, game_id FROM {cls.table_name} WHERE game_id = ?;
        """
        query_params = (game_id,)
        players_data = execute_query(select_players, query_params).fetchall()
        players = [Player(*player_data) for player_data in players_data]
        return players
