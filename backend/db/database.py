from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (AsyncSession,
                                    async_sessionmaker,
                                    create_async_engine)

from core.config import settings
from db.models import Base

async_engine = create_async_engine(
    url=settings.ASYNC_DATABASE_URL,
    echo=settings.DEBUG,
)

async_session_maker = async_sessionmaker(
    bind=async_engine,
    class_=AsyncSession,
    expire_on_commit=False
)


async def init_models():
    """Создание БД."""
    async with async_engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)


async def get_session() -> AsyncGenerator[AsyncSession, None]:
    """Подключение к БД."""
    async with async_session_maker() as session:
        yield session
