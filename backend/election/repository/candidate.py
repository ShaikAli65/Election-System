from repository.interface import Repository


class CandidateRepository(Repository):
    async def create(self, item):
        pass

    async def read(self, item_id):
        pass

    async def update(self, item_id, item):
        pass

    async def delete(self, item_id):
        pass
