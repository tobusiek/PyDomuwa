import sqlite3
from sqlite3 import Cursor

connection = sqlite3.connect('database.db')
cursor = connection.cursor()


def execute_query(query: str, query_params: tuple = ()) -> Cursor:
    return cursor.execute(query, query_params)


def execute_query_and_commit(query: str, query_params: tuple = ()) -> None:
    execute_query(query, query_params)
    connection.commit()
