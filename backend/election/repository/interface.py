from abc import ABC, abstractmethod

from db.database import DB


class Repository(ABC):
    def __init__(self, _db: DB):
        self._database = _db

    @abstractmethod
    async def create(self, item):...
    @abstractmethod
    async def read(self, item_id):...
    @abstractmethod
    async def update(self, item_id, item):...
    @abstractmethod
    async def delete(self, item_id):...
