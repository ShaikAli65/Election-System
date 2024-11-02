from sqlalchemy.ext.asyncio import AsyncSession

from repository.interface import Repository


class VoterRepository(Repository):

    async def add_voter(self):
        async with self._database() as async_session:
            async_session: AsyncSession

    async def create(self, item):
        async with self._database() as async_session:
            async_session: AsyncSession

    async def read(self, item_id):
        async with self._database() as async_session:
            async_session: AsyncSession

    async def update(self, item_id, item):
        async with self._database() as async_session:
            async_session: AsyncSession

    async def delete(self, item_id):
        async with self._database() as async_session:
            async_session: AsyncSession
