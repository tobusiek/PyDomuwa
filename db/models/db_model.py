from abc import ABC, abstractmethod


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

    @classmethod
    @abstractmethod
    def get_by_id(cls, model_id: int):
        ...
