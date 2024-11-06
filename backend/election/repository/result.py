from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from election.db.schemas import ElectionResultSchema
from election.repository.interface import Repository


class ResultRepository(Repository):
    async def create(self, item):
        async with self.database() as async_session:
            async_session: AsyncSession
            async_session.add(item)

    async def read(self, item_id):
        async with self.database() as async_session:
            async_session: AsyncSession
            stmt = select(ElectionResultSchema).where(ElectionResultSchema.election_id == item_id)
            result = await async_session.execute(stmt)
            return result.scalars().all()

    async def update(self, item_id, item):
        async with self.database() as async_session:
            async_session: AsyncSession

    async def delete(self, item_id):
        async with self.database() as async_session:
            async_session: AsyncSession

