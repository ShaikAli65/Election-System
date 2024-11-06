from dataclasses import asdict

from sqlalchemy import and_, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from election.core.models.poll import BallotEntry
from election.db.schemas import BallotSchema
from election.repository.interface import Repository


class BallotRepository(Repository):
    async def create(self, item):
        async with self.database() as async_session:
            async_session: AsyncSession

    async def read(self, item_id) -> BallotSchema:
        poll_id, user_id = item_id
        async with self.database() as async_session:
            async_session: AsyncSession
            smqt = select(BallotSchema).where(
                and_(
                    BallotSchema.election_id == poll_id,
                    BallotSchema.candidate_id == user_id,
                )
            )
            interm_result = await async_session.execute(smqt)
            return interm_result.scalars().first()

    async def update(self, item_id, item):
        raise ValueError("ballot cannot be updated")
        # async with self.database() as async_session:
        #     async_session: AsyncSession

    async def delete(self, ballot_id):
        raise ValueError("ballot cannot be deleted")
        # async with self.database() as async_session:
        #     async_session: AsyncSession
        #     query = delete(BallotSchema).where(BallotSchema.ballot_id == ballot_id)
        #     await async_session.execute(query)
        #     return await async_session.commit()

    async def entry_vote(self, entry: BallotEntry):
        async with self.database() as async_session:
            async_session: AsyncSession
            schema = BallotSchema(**asdict(entry))
            return async_session.add(schema)

    async def read_election(self, poll_id):
        async with self.database() as async_session:
            async_session: AsyncSession
            stmt = select(BallotSchema).where(BallotSchema.election_id == poll_id)
            results = await async_session.execute(stmt)
            return results.scalars().fetchall()
