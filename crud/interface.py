from abc import ABC, abstractmethod
from typing import Any, Coroutine, TypeVar, Generic, Type, Sequence

from sqlalchemy.ext.asyncio import AsyncSession
from core import Base

T = TypeVar("T", bound=Base) # type: ignore

class CRUDInterface(ABC, Generic[T]):
    """
    Интерфейс для реализации операций CRUD.
    """

    @abstractmethod
    async def create(
        self,
        obj: T,
        session: AsyncSession,
    ) -> T:
        pass

    @abstractmethod
    async def read(
        self,
        obj_type: Type[T],
        obj_id: int,
        session: AsyncSession,
    ) -> Coroutine[Any, Any, T | None]:
        pass

    @abstractmethod
    async def read_all(
        self,
        obj_type: Type[T],
        session: AsyncSession,
    ) -> Coroutine[Any, Any, Sequence[T]]:
        pass

    @abstractmethod
    async def update(
        self,
        obj_type: Type[T],
        obj_id: int,
        new_data: dict[str, Any],
        session: AsyncSession,
    ) -> T | None:
        pass

    @abstractmethod
    async def delete(
        self,
        obj_type: Type[T],
        obj_id: int,
        session: AsyncSession,
    ) -> T | None:
        pass
