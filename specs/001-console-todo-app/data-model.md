# Data Model: Phase I In-Memory Python Console Todo Application

## Primary Entity: Todo

### Fields
- **id**: `int` (auto-generated, unique, sequential starting from 1, never reused after deletion)
- **title**: `str` (required, max 100 characters, non-empty)
- **description**: `str` (optional, max 500 characters, can be None or empty string)
- **status**: `str` (enum: "pending", "in_progress", "completed"; defaults to "pending" for new todos)
- **priority**: `str` (enum: "low", "medium", "high"; required, no default)
- **created_at**: `datetime` (auto-generated, ISO 8601 format, UTC timezone)

### Validation Rules
- Title: Required, not empty, max 100 characters
- Description: Optional, max 500 characters
- Status: Must be one of "pending", "in_progress", "completed"
- Priority: Must be one of "low", "medium", "high"
- ID: Auto-generated, unique, sequential, never reused after deletion

### State Transitions
- New todo: status automatically set to "pending"
- Status can transition between any of the three states via update operations
- No restrictions on state transitions (users can move from any status to any other)

### Relationships
- No relationships with other entities (standalone entity)

## Storage Model
- **In-memory storage**: `dict[int, Todo]` where key is the todo ID
- **ID counter**: `int` starting from 1, incremented for each new todo, never decremented
- **Thread safety**: Not required (single-threaded application per Phase I constraints)

## Pydantic Model Definition
```python
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
    id: int
    title: str = Field(..., min_length=1, max_length=100)
    description: Optional[str] = Field(None, max_length=500)
    status: TodoStatus = TodoStatus.PENDING
    priority: TodoPriority
    created_at: datetime
```