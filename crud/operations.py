from typing import Any, TypeVar, Type, Coroutine, Sequence

from sqlalchemy import asc, select
from sqlalchemy.ext.asyncio import AsyncSession


from core import Base
from .interface import CRUDInterface


T = TypeVar("T", bound=Base)  # type: ignore


class CRUDOperations(CRUDInterface[T]):
	async def create(
    	self,
     	obj_type: Type[T],
      	session: AsyncSession,
       	data: dict
    ) -> T:
		obj = obj_type(**data)
		session.add(obj)
		await session.commit()
		await session.refresh(obj)
		return obj

	async def read(
		self,
		obj_type: Type[T],
		obj_id: int,
		session: AsyncSession,
	) -> Coroutine[Any, Any, T | None]:
		return await session.get(obj_type, obj_id)

	async def read_all(
		self,
		obj_type: Type[T],
		session: AsyncSession,
	) -> Coroutine[Any, Any, Sequence[T]]:
		result = await session.execute(select(obj_type).order_by(asc(obj_type.id)))
		return result.scalars().all()

	async def update(
		self,
		obj_type: Type[T],
		obj_id: int,
		new_data: dict[str, Any],
		session: AsyncSession,
	) -> T | None:
		data_from_db = await self.read(
            obj_type,
            obj_id,
            session
        )
		if not data_from_db:
			return None
		for field, value in new_data.items():
			if hasattr(data_from_db, field):
				setattr(data_from_db, field, value)
		session.add(data_from_db)
		await session.commit()
		await session.refresh(data_from_db)
		return data_from_db

	async def delete(
		self,
		obj_type: Type[T],
		obj_id: int,
		session: AsyncSession,
	) -> T | None:
		data_to_delete = await self.read(
            obj_type,
            obj_id,
            session
        )
		if not data_to_delete:
			return None
		await session.delete(data_to_delete)
		await session.commit()
		return data_to_delete

crud_operations = CRUDOperations()