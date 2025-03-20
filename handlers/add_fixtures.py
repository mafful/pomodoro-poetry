from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from .tasks import (
    category_crud_operations,
    task_crud_operations,
)
from models import Category, Task
from core import get_async_session
from work_with_SQLite.fixtures import fixture_categories, fixture_tasks

router = APIRouter(prefix="/fixtures", tags=["/fixtures"])


@router.post("/add_fixtures")
async def add_fixtures(session: AsyncSession = Depends(get_async_session)):
    """
    Adds predefined categories and tasks to the database.
    """
    # Insert Categories
    for category in fixture_categories:
        await category_crud_operations.create(Category, session, category)

    # Insert Tasks
    for task in fixture_tasks:
        await task_crud_operations.create(Task, session, task)

    await session.commit()  # Ensure all data is saved
    return {"message": "Fixtures added successfully"}