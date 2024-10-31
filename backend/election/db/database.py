# database.py
from sqlalchemy.ext.asyncio import async_sessionmaker, create_async_engine
from sqlalchemy.ext.declarative import declarative_base

from core.constants import get_dbconfig

# Base class for models
Base = declarative_base()

# global reference for sqlalchemy engine as per the spec
_engine = None


_AsyncSessionLocal: async_sessionmaker | None = None


async def get_db():
    async with _AsyncSessionLocal() as _s:
        yield _s


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
