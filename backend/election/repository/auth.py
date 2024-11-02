from uuid import UUID

from core.models.user import UserLoggedInCookie
from repository.interface import Repository


class AuthRepository(Repository):

    async def read(self, item_id):
        async with self._database() as database:
            database: dict[UUID, UserLoggedInCookie]
            return database.get(item_id)

    async def update(self, item_id, item: UserLoggedInCookie):
        async with self._database() as database:
            database: dict[UUID, UserLoggedInCookie]
            database[item_id] = item

    async def delete(self, item_id):
        async with self._database() as database:
            database: dict[UUID, UserLoggedInCookie]
            return database.pop(item_id)

    async def create(self, item: tuple[UUID, UserLoggedInCookie]):
        async with self._database() as database:
            database: dict[UUID, UserLoggedInCookie]
            database[item[0]] = item[1]
