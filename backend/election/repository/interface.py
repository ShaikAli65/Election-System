from abc import ABC, abstractmethod

from db.database import DB


class Repository(ABC):
    def __init__(self, _db: DB):
        self._async_database = _db

    @abstractmethod
    def create(self, item):...
    @abstractmethod
    def read(self, item_id):...
    @abstractmethod
    def update(self, item_id, item):...
    @abstractmethod
    def delete(self, item_id):...
