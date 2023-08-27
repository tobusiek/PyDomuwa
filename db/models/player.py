from typing import Optional

from db.database import execute_query, execute_query_and_commit
from db.models.db_model import DbModel


class Player(DbModel):
    table_name = "player"

    def __init__(self, name: str, player_id: int = 0, score: float = 0.0, game_id: int = None):
        super().__init__(player_id)
        self.name = name
        self.score = score
        self.game_id = game_id

    def update_score(self, points: float) -> None:
        self.score += points
        update_player_score = f"""
        UPDATE {self.table_name} SET score = ? WHERE id = ?;
        """
        player_data = (self.score, self.id)
        execute_query_and_commit(update_player_score, player_data)

    def clear_score(self) -> None:
        self.score = 0.0
        # TODO: generate sql for this

    @classmethod
    def create_table(cls):
        # TODO: FK game_id, IDX name
        create_player_table = f"""
        CREATE TABLE IF NOT EXISTS {cls.table_name} (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            score REAL NOT NULL,
            game_id INTEGER
        );
        """
        execute_query_and_commit(create_player_table)

    def save(self):
        insert_player = f"""
        INSERT INTO {self.table_name} (name, score, game_id) VALUES (?, ?, ?);
        """
        player_data = (self.name, self.score, self.game_id)
        execute_query_and_commit(insert_player, player_data)

    @classmethod
    def get_all(cls) -> list["Player"]:
        select_players = f"""
        SELECT id, name, score, game_id FROM {cls.table_name};
        """
        players_data = execute_query(select_players).fetchall()
        if not players_data:
            return []
        players = [Player(name, player_id, score, game_id) for player_id, name, score, game_id in players_data]
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
        return Player(**player_data)

    @classmethod
    def get_by_name(cls, name: str) -> Optional["Player"]:
        select_player = f"""
        SELECT name, id, score, game_id FROM {cls.table_name} WHERE name = ?;
        """
        query_params = (name,)
        player_data = execute_query(select_player, query_params).fetchone()
        if not player_data:
            return None
        return Player(**player_data)
