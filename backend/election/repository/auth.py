from repository.interface import Repository


class AuthRepository(Repository):

    def read(self, item_id):
        pass

    def update(self, item_id, item):
        pass

    def delete(self, item_id):
        pass

    def create(self, item):
        pass

    def voter_logged_in(self):
        ...
