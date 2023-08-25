from abc import ABC, abstractmethod

from db.database import execute_query, execute_query_and_commit


class DbModel(ABC):
    table_name: str

    def __init__(self, model_id: int):
        self.id = model_id

    @classmethod
    @abstractmethod
    def create_table(cls) -> None:
        ...

    @abstractmethod
    def save(self) -> None:
        ...

    @classmethod
    @abstractmethod
    def get_all(cls) -> list:
        ...


class Game(DbModel):
    table_name = "game"

    def __init__(self, name: str, game_id: int = 0):
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
        execute_query(create_game_table)

    def save(self) -> None:
        insert_game = """
        INSERT INTO game (name) VALUES (?);
        """
        game_data = (self.name,)
        execute_query_and_commit(insert_game, game_data)

    @classmethod
    def get_all(cls) -> list["Game"]:
        select_games = f"""
        SELECT id, name FROM game;
        """
        games_data = execute_query(select_games).fetchall()
        games = [Game(game_id, name) for game_id, name in games_data]
        return games


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
        INSERT INTO {self.table_name} (name) VALUES (?);
        """
        player_data = (self.name,)
        execute_query_and_commit(insert_player, player_data)

    @classmethod
    def get_all(cls) -> list["Player"]:
        select_players = f"""
        SELECT id, name, score, game_id FROM {cls.table_name};
        """
        players_data = execute_query(select_players).fetchall()
        players = [Player(player.id, player.name, player.score, player.game_id) for player in players_data]
        return players


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
