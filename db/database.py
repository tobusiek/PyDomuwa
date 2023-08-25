import sqlite3
from sqlite3 import Cursor

connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def execute_query(query: str, params: tuple = None) -> Cursor:
    return cursor.execute(query, params)


def execute_query_and_commit(query: str, params: tuple = None) -> None:
    execute_query(query, params)
    connection.commit()
