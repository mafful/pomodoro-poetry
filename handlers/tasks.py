from typing import List, Type
from fastapi import APIRouter, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from core import get_async_session
from crud import CRUDOperations
from models import Category, Task

from sqlalchemy.ext.asyncio import AsyncSession


templates = Jinja2Templates(directory="templates")

# Base router
router = APIRouter()

# CRUD operations for different models
task_crud_operations = CRUDOperations[Task]()
category_crud_operations = CRUDOperations[Category]()


def create_crud_router(
    entity_name: str,
    create_model: Type[BaseModel],  # ✅ Pydantic model for creation
    response_model: Type[BaseModel],  # ✅ Pydantic model for response
    db_model: Type,
    service: CRUDOperations,
) -> APIRouter:
    """
    Dynamically creates a CRUD router for a given entity.

    :param entity_name: Name of the entity (e.g., "Task", "Category")
    :param create_model: Pydantic model type for request validation
    :param response_model: Pydantic model type for response serialization
    :param db_model: SQLAlchemy ORM model type
    :param service: Instance of CRUDOperations for DB interactions
    :return: APIRouter instance with CRUD routes
    """
    prefix = (
        f"/{entity_name.lower()}s"
        if not entity_name.endswith("y")
        else f"/{entity_name.lower()[:-1]}ies"
    )
    router = APIRouter(prefix=prefix, tags=[prefix.capitalize()])

    @router.get("/", response_model=List[response_model])  # ✅ Correct response model
    async def get_all(session: AsyncSession = Depends(get_async_session)):
        return await service.read_all(db_model, session)

    @router.post("/", response_model=response_model)  # ✅ Correct response model
    async def create(
        item: create_model,  # ✅ Use correct Pydantic model for input # type: ignore
        session: AsyncSession = Depends(get_async_session)
    ):
        try:
            obj = await service.create(db_model, session, item.dict())
            return obj
        except Exception as e:
            raise HTTPException(status_code=400, detail=str(e))

    @router.get("/{item_id}", response_model=response_model)  # ✅ Correct response model
    async def get_one(item_id: int, session: AsyncSession = Depends(get_async_session)):
        obj = await service.read(db_model, item_id, session)
        if obj is None:
            raise HTTPException(status_code=404, detail=f"{entity_name} not found")
        return obj

    @router.put("/{item_id}", response_model=response_model)  # ✅ Correct response model
    async def update(
        item_id: int,
        updated_item: create_model,  # ✅ Use correct Pydantic model for input # type: ignore
        session: AsyncSession = Depends(get_async_session),
    ):
        updated_obj = await service.update(
            db_model, item_id, updated_item.dict(), session
        )
        if updated_obj is None:
            raise HTTPException(
                status_code=404, detail=f"{entity_name} not found or update failed"
            )
        return updated_obj

    @router.delete("/{item_id}")
    async def delete(item_id: int, session: AsyncSession = Depends(get_async_session)):
        deleted_obj = await service.delete(db_model, item_id, session)
        if deleted_obj is None:
            raise HTTPException(status_code=404, detail=f"{entity_name} not found")
        return {"message": f"{entity_name} deleted successfully"}

    return router


# Create routers dynamically
task_router = create_crud_router(
    "Task",
    Task.CreatePydanticModel,
    Task.ResponsePydanticModel,
    Task,
    task_crud_operations
)
category_router = create_crud_router(
    "Category",
    Category.CreatePydanticModel,
    Category.ResponsePydanticModel,
    Category,
    category_crud_operations
)

# Register routers
router.include_router(task_router)
router.include_router(category_router)
