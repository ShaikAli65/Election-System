import datetime
from typing import Annotated

import sqlalchemy.exc
from fastapi import Cookie, Depends, HTTPException
from jose import JWTError, jwt
from starlette import status
from starlette.requests import Request

from election.core.constants import get_google_oauth_creds, get_jwt_config
from election.core.models.user import User, UserCredentials, UserLoggedInCookie
from election.db.database import AsyncDB, DictDB, db_session_factory
from election.repository.auth import AuthRepository
from election.repository.user import UserRepository


class AuthContext:
    def __init__(self, auth_repo: AuthRepository, user_repo: UserRepository):
        self._auth_repo = auth_repo
        self._user_repo = user_repo
        self._user: User | None = None

    async def new_user_logged_in(self, user_creds: UserCredentials):
        if await self._auth_repo.read(user_creds.user_id) is not None:
            # if we found an active entry in our auth repository then no need to anything
            self._user = await self._user_repo.read(user_creds.user_id)
            return

        self._user = self._user_repo.from_credentials(user_creds=user_creds)

        if not await self._user_repo.read(self._user.user_id):
            # if user not found then create an entry automatically
            try:
                await self._user_repo.create(self._user)
            except sqlalchemy.exc.IntegrityError as exp:
                print(exp)
                raise

        cookie = await self.generate_cookie()
        await self._auth_repo.create((self.user.user_id, cookie))

    async def from_cookie(self, user_cookie: UserLoggedInCookie):
        user_model = self.verify_jwt(user_cookie.access_token)
        self._user = User(**user_model)

        stored_user_cookie = await self._auth_repo.read(self._user.user_id)
        if stored_user_cookie is None:
            raise ValueError('cookie not valid')

        assert user_cookie == stored_user_cookie, "cookie not matched"

    async def generate_cookie(self):
        existing_cookie = await self._auth_repo.read(self.user.user_id)
        if existing_cookie:
            return existing_cookie

        to_encode = self.user.model_dump()
        jwt_config = get_jwt_config()
        expire = datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=jwt_config.expire_time_min)
        to_encode['user_id'] = str(to_encode['user_id'])
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, jwt_config.secret_key, algorithm=jwt_config.algorithm)
        return UserLoggedInCookie(access_token=encoded_jwt)

    @staticmethod
    def verify_jwt(token: str):
        jwt_context = get_jwt_config()
        payload = jwt.decode(token, jwt_context.secret_key, algorithms=[jwt_context.algorithm])
        return payload

    @property
    def user(self):
        return self._user


# dependencies

async def get_auth_context(request: Request) -> AuthContext:
    token = request.headers.get('access_token')
    if not token:
        print("token not found", list(request.headers.items()))
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    cookie = UserLoggedInCookie(access_token=token)

    u_repo = UserRepository(AsyncDB(db_session_factory))
    a_repo = AuthRepository(DictDB())
    context = AuthContext(a_repo, u_repo)

    try:
        await context.from_cookie(cookie)
    except ValueError as ve:
        raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(ve))
    except JWTError as je:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token") from je

    return context

Authenticator = Annotated[AuthContext, Depends(get_auth_context)]


async def sign_in_user(user_creds: UserCredentials):

    oauthcreds = get_google_oauth_creds()
    try:
        assert oauthcreds.client_id == user_creds.authorized_party, "Invalid Client Id from JS"
    except AssertionError:
        raise HTTPException(status.HTTP_401_UNAUTHORIZED, detail="oauth client id provided is not valid")

    u_repo = UserRepository(AsyncDB(db_session_factory))
    a_repo = AuthRepository(DictDB())

    context = AuthContext(a_repo, u_repo)

    await context.new_user_logged_in(user_creds)
    # try:
    # except Exception as e:
    #     raise HTTPException(status_code=status.HTTP_406_NOT_ACCEPTABLE, detail=str(e))

    return context
