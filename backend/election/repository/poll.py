from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from election.db.schemas import ElectionSchema
from election.repository.interface import Repository


class PollRepository(Repository):

    def __init__(self, _db):
        super().__init__(_db)

    async def create(self, item: ElectionSchema):
        async with self.database() as async_session:
            async_session: AsyncSession
            async_session.add(item)

    async def read(self, item_id) -> ElectionSchema:
        async with self.database() as async_session:
            async_session: AsyncSession
            result = await async_session.execute(
                select(ElectionSchema).filter_by(election_id=item_id)
            )
            return result.scalars().first()  # Get the first result

    async def update(self, item_id, item: ElectionSchema):
        async with self.database() as async_session:
            async_session: AsyncSession
            existing_item = await self.read(item_id)
            if existing_item is None:
                raise NoResultFound("Election not found.")

            existing_item.election_id = item.election_id
            existing_item.description = item.description
            existing_item.start_date = item.start_date
            existing_item.end_date = item.end_date
            existing_item.total_candidates = item.total_candidates
            existing_item.total_voters = item.total_voters
            existing_item.title = item.title
            existing_item.election_status = item.election_status
            existing_item.validation_regex = item.validation_regex
            await async_session.merge(existing_item)

    async def delete(self, item_id):
        async with self.database() as async_session:
            async_session: AsyncSession
            # Fetch the existing item first
            existing_item = await self.read(item_id)
            if existing_item is None:
                raise NoResultFound("Election not found.")

            await async_session.delete(existing_item)  # Delete the existing item

    async def increment_total_voters(self, poll_id):
        async with self.database() as async_session:
            async_session: AsyncSession
            result = await async_session.execute(
                select(ElectionSchema).filter_by(election_id=poll_id)
            )
            result = result.scalars().first()  # Get the first result
            result.total_voters += 1
