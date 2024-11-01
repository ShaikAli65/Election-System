from core.models.person import UserCredentials, UserLoggedInCookie
from db.database import DictDB
from repository.auth import AuthRepository


class AuthContext:
    def __init__(self, authrepository: AuthRepository):
        self._authrepo = authrepository

    async def new_voter_logged_in(self, form_data) -> UserLoggedInCookie:
        ...


async def get_auth_context() -> AuthContext:
    ...


async def sign_in_user(user_creds: UserCredentials):

    repo = AuthRepository(DictDB())
    context = AuthContext(repo)
    # await context.new_voter_logged_in()erws
