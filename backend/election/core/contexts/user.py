from typing import Annotated

from fastapi.params import Depends

from core.contexts.auth import Authenticator
from core.models.user import User
from db.database import AsyncDB, db_session_factory
from repository.user import UserRepository


class UserContext:
    def __init__(self, user: User, repository: UserRepository):
        self.user = user
        self.repository = repository

    def __repr__(self):
        return f"<UserContext({self.user}, {self.repository})>"


async def get_user_context(authenticator: Authenticator):

    async_db = AsyncDB(db_session_factory)
    repository = UserRepository(async_db)
    vc = UserContext(authenticator.user, repository)
    return vc

userContext = Annotated[UserContext, Depends(get_user_context)]
