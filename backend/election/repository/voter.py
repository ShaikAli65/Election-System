from sqlalchemy.ext.asyncio import AsyncSession

from repository.interface import Repository


class VoterRepository(Repository):

    async def add_voter(self):
        ...
