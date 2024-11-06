from sqlalchemy import and_, delete, select, update
from sqlalchemy.exc import MultipleResultsFound
from sqlalchemy.ext.asyncio import AsyncSession

from election.core.models.user import VoterInDb
from election.db.schemas import VoterSchema
from election.repository.interface import Repository


class VoterRepository(Repository):

    async def create(self, item: VoterInDb):
        async with self.database() as async_session:
            async_session: AsyncSession
            voter = VoterSchema(**item.model_dump())
            async_session.add(voter)
            return voter

    async def read(self, ids) -> VoterInDb | None:
        voter_id, election_id = ids
        async with self.database() as async_session:
            async_session: AsyncSession
            query = select(VoterSchema).where(
                and_(
                    VoterSchema.user_id == voter_id,
                    VoterSchema.election_id == election_id,
                )
            )

            voter_entry = (await async_session.execute(query)).first()
            if voter_entry:
                voter_entry = voter_entry.tuple()[0]
                return VoterInDb.model_validate(voter_entry)
            return None

    async def update(self, ids, voter_update: VoterInDb):
        voter_id, election_id = ids
        async with self.database() as async_session:
            async_session: AsyncSession
            query = update(VoterSchema).where(
                and_(
                    VoterSchema.user_id == voter_id,
                    VoterSchema.election_id == election_id,
                )
            ).values(**voter_update.model_dump())
            await async_session.execute(query)
            return await self.read(ids)

    async def delete(self, voter_id):
        async with self.database() as async_session:
            async_session: AsyncSession
            query = delete(VoterSchema).where(VoterSchema.user_id == voter_id)
            await async_session.execute(query)

    async def mark_voted(self, voter_id, poll_id):
        async with self.database() as async_session:
            async_session: AsyncSession
            stmt = select(VoterSchema).where(
                and_(
                    VoterSchema.user_id == voter_id,
                    VoterSchema.election_id == poll_id,
                )
            )
            try:
                result = (await async_session.execute(stmt)).scalar_one_or_none()  # Fetches a single instance or None
                result.has_voted = True
            except MultipleResultsFound as mrf:
                raise ReferenceError("wtf") from mrf
