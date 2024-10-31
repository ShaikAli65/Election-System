from sqlalchemy.ext.asyncio import AsyncSession


class Repository:
    def __int__(self, sqlalchemy_session:AsyncSession):
        self._database = sqlalchemy_session
