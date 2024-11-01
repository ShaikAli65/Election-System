from fastapi.security import OAuth2PasswordRequestForm

from core.models.person import UserLoggedInCookie
from repository.auth import AuthRepository


class AuthContext:
    def __int__(self, authrepository: AuthRepository):
        self._authrepo = authrepository

    def new_voter_logged_in(self, form_data: OAuth2PasswordRequestForm) -> UserLoggedInCookie:

        ...


def get_auth_context() -> AuthContext:
    ...
