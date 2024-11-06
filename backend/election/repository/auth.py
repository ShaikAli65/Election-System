from uuid import UUID

from election.core.models.user import UserLoggedInCookie
from election.repository.interface import Repository


class AuthRepository(Repository):

    async def read(self, item_id):
        async with self.database() as database:
            database: dict[UUID, UserLoggedInCookie]
            return database.get(str(item_id))

    async def update(self, item_id, item: UserLoggedInCookie):
        async with self.database() as database:
            database: dict[UUID, UserLoggedInCookie]
            database[str(item_id)] = item

    async def delete(self, item_id):
        async with self.database() as database:
            database: dict[UUID, UserLoggedInCookie]
            return database.pop(str(item_id))

    async def create(self, item: tuple[UUID, UserLoggedInCookie]):
        async with self.database() as database:
            database: dict[UUID, UserLoggedInCookie]
            database[str(item[0])] = item[1]
