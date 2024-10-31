# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import session

# Replace with your existing database connection details
DATABASE_URL = "postgresql://postgres:0@localhost:5433/postgres"

# Create database engine
engine = create_async_engine(DATABASE_URL)

# Create session
AsyncSessionLocal = async_sessionmaker(
    bind=engine,
    expire_on_commit=False,
)

# Base class for models
Base = declarative_base()


async def get_db():
    async with AsyncSessionLocal() as _s:
        yield _s
