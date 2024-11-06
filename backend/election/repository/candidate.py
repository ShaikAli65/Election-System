from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from election.db.schemas import CandidateSchema
from election.repository.interface import Repository


class CandidateRepository(Repository):
    async def create(self, item: CandidateSchema):
        async with self.database() as async_session:
            async_session: AsyncSession
            return async_session.add(item)

    async def read(self, item_id):
        async with self.database() as async_session:
            async_session: AsyncSession

    async def update(self, item_id, item):
        async with self.database() as async_session:
            async_session: AsyncSession
            query = update(CandidateSchema).where(
                CandidateSchema.candidate_id == item_id
            ).values(
                **item.model_dump()
            )
            await async_session.execute(query)

    async def delete(self, item_id):
        async with self.database() as async_session:
            async_session: AsyncSession
            query = delete(CandidateSchema).where(CandidateSchema.candidate_id == item_id)
            await async_session.execute(query)

    async def get_candidates_in_election(self, poll_id):
        async with self.database() as async_session:
            async_session: AsyncSession
            query = select(
                CandidateSchema
            ).where(
                CandidateSchema.election_id == poll_id
            )
            result = await async_session.execute(query)
            candidates = result.scalars().all()
            return candidates
