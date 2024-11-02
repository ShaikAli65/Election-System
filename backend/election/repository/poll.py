from db.database import AsyncDB
from repository.interface import Repository


class PollRepository(Repository):

    def __init__(self, _db: AsyncDB):
        super().__init__(_db)

    async def create(self, item):
        async with self._database() as async_session:
            ...

    def read(self, item_id):
        pass

    def update(self, item_id, item):
        pass

    def delete(self, item_id):
        pass
