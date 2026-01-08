from datetime import datetime
from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum


class TodoStatus(str, Enum):
    PENDING = "pending"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"


class TodoPriority(str, Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"


class Todo(BaseModel):
    """
    Represents a task the user needs to complete.

    Attributes:
        id: Unique identifier (auto-generated integer starting from 1, incrementing sequentially; never reused after deletion)
        title: Title describing the task (required, max 100 characters)
        description: Optional detailed description (max 500 characters)
        status: Current status (pending/in_progress/completed)
        priority: Priority level (low/medium/high)
        created_at: Creation timestamp (auto-generated, ISO 8601 format)
    """
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: TodoStatus = TodoStatus.PENDING
    priority: TodoPriority
    created_at: datetime