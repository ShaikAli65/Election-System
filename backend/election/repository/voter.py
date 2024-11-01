from repository.interface import Repository


class VoterRepository(Repository):

    async def add_voter(self):
        async with self._async_database as async_session:
            # async_session: AsyncSession
            ""

    def create(self, item):...
    def read(self, item_id):...
    def update(self, item_id, item):...
    def delete(self, item_id):...
