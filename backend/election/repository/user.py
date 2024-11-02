import uuid

from sqlalchemy import delete, select, update
from sqlalchemy.ext.asyncio import AsyncSession

from core.models.user import User, UserCredentials
from db.schemas import Authentication
from repository.interface import Repository


class UserRepository(Repository):

    async def create(self, user: User):
        async with self._database() as async_session:
            async_session: AsyncSession
            new_user = Authentication(**user.model_dump())
            async_session.add(new_user)
            await async_session.commit()
            await async_session.refresh(new_user)
            return new_user

    @staticmethod
    def from_credentials(user_creds: UserCredentials) -> User:
        try:
            uuid_id = uuid.UUID(int=int(user_creds.user_id))
        except Exception as e:
            raise ValueError("can't convert a valid uuid from given creds") from e

        return User(
            user_id=uuid_id,
            email_id=user_creds.email,
            user_name=user_creds.name,
        )

    async def read(self, user_id):
        async with self._database() as async_session:
            async_session: AsyncSession
            result = await async_session.execute(select(Authentication).filter_by(user_id=user_id))
            return result.scalars().first()

    async def update(self, user_id, user_model: User):
        async with self._database() as async_session:
            async_session: AsyncSession
            query = update(Authentication).where(Authentication.user_id == user_id).values(**user_model.model_dump())
            await async_session.execute(query)
            await async_session.commit()
            return await self.read(user_id)

    async def delete(self, user_id):
        async with self._database() as async_session:
            async_session: AsyncSession
            query = delete(Authentication).where(Authentication.user_id == user_id)
            await async_session.execute(query)
            await async_session.commit()
            return {"message": "Authentication record deleted successfully"}
