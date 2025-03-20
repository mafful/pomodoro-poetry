from pydantic import BaseModel
from sqlalchemy import ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core import Base


# ---- Category Model ----
class Category(Base):
    name: Mapped[str] = mapped_column(nullable=False)

    # Relationship to Task
    tasks: Mapped[list["Task"]] = relationship("Task", back_populates="category")


    # ✅ Separate Pydantic models for input and output
    class CreatePydanticModel(BaseModel):  # Used for creating a task (no ID required)
        name: str

    class ResponsePydanticModel(BaseModel):  # Used for returning a task (ID included)
        id: int
        name: str


# ---- Task Model ----
class Task(Base):
    name: Mapped[str] = mapped_column(nullable=False)
    pomodoro_count: Mapped[int] = mapped_column(nullable=False, default=1)
    category_id: Mapped[int] = mapped_column(nullable=False)

    # Foreign key linking to Category
    category_id: Mapped[int] = mapped_column(ForeignKey("categories.id"), nullable=False)

    # Relationship to Category
    category: Mapped["Category"] = relationship("Category", back_populates="tasks")


    # ✅ Separate Pydantic models for input and output
    class CreatePydanticModel(BaseModel):  # Used for creating a task (no ID required)
        name: str
        pomodoro_count: int
        category_id: int

    class ResponsePydanticModel(BaseModel):  # Used for returning a task (ID included)
        id: int
        name: str
        pomodoro_count: int
        category_id: int
