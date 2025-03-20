from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import (
    AsyncSession,
    create_async_engine,
    async_sessionmaker,
)
from sqlalchemy.orm import (
    Mapped,
    mapped_column,
    as_declarative,
    declared_attr,
)

from .settings import settings

@as_declarative()
class Base:
    """
    Mixin that provides a primary key and automatic table naming.
    """

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)

    @declared_attr.directive
    @classmethod
    def __tablename__(cls) -> str:
        """Generate a pluralized table name based on class name."""
        name = cls.__name__.lower()
        if name.endswith('y'):
            return f'{name[:-1]}ies'  # Category → categories
        return f'{name}s'  # Task → tasks, User → users


engine = create_async_engine(settings.database_url)
AsyncSessionLocal = async_sessionmaker(bind=engine)


async def get_async_session() -> AsyncGenerator[AsyncSession, None]:
    """
    Генератор асинхронных сессий для работы с базой данных.

    Parameters
    ----------
    None

    Yields
    ------
    AsyncSession
        Экземпляр асинхронной сессии, используемый для взаимодействия с БД.

    """

    async with AsyncSessionLocal() as async_session:
        yield async_session
