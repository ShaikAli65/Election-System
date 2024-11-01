# database.py
from contextlib import asynccontextmanager
from typing import AsyncGenerator, Callable

from sqlalchemy.ext.asyncio import AsyncSession, async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from core.constants import get_dbconfig

# Base class for models
Base = declarative_base()

# global reference for sqlalchemy engine as per the spec
_engine = None


_AsyncSessionLocal: async_sessionmaker | None = None


def db_session_factory() -> AsyncSession:
    global _AsyncSessionLocal
    return _AsyncSessionLocal()


def get_alchemy_engine():
    global _engine
    return _engine


class DB:
    def __init__(self):
        ...


class AsyncDB(DB):
    """
    Just a context manager wrapper around :class:`AsyncSession`
    """
    __slots__ = ('_sqlalchemy_session_maker',)

    def __init__(self, async_session_maker: Callable[[], AsyncSession]):
        super().__init__()
        self._sqlalchemy_session_maker = async_session_maker

    @asynccontextmanager
    async def start(self) -> AsyncGenerator[AsyncSession, None]:
        session = None
        try:
            session = self._sqlalchemy_session_maker()
            yield session
        finally:
            if session:
                await session.close()


class DictDB(DB):
    session_data = {}

    def __init__(self):
        super().__init__()
        self._dict = DictDB.session_data


async def initialize_database():
    global _engine, _AsyncSessionLocal
    dbconfig = get_dbconfig()
    _engine = create_async_engine(
        dbconfig.url,
        **dbconfig.engine_args
    )
    _AsyncSessionLocal = async_sessionmaker(
        bind=_engine,
        expire_on_commit=False,
    )