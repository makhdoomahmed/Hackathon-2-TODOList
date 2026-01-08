# Todo Service Contract

## Overview
This contract defines the interface and behavior for the TodoService class that handles all business logic for the console todo application.

## Service Interface

### TodoService Class

```python
from typing import List, Optional, Dict
from datetime import datetime
from src.models import Todo, TodoStatus, TodoPriority

class TodoService:
    def __init__(self):
        """Initialize the service with empty storage and ID counter"""
        pass

    def add_todo(self, title: str, description: Optional[str], priority: TodoPriority) -> Todo:
        """
        Create a new todo with the given parameters.

        Args:
            title: Required title (1-100 characters)
            description: Optional description (max 500 characters)
            priority: Priority level (low, medium, high)

        Returns:
            Todo: The created todo with auto-generated ID and timestamp

        Raises:
            ValueError: If title is invalid (empty or too long)
        """
        pass

    def get_all_todos(self) -> List[Todo]:
        """
        Retrieve all todos sorted by ID.

        Returns:
            List[Todo]: All todos in the system, sorted by ID
        """
        pass

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Retrieve a specific todo by its ID.

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            Todo: The todo if found, None otherwise
        """
        pass

    def update_todo(self, todo_id: int, title: Optional[str] = None, description: Optional[str] = None,
                   status: Optional[TodoStatus] = None, priority: Optional[TodoPriority] = None) -> Optional[Todo]:
        """
        Update specified fields of an existing todo.

        Args:
            todo_id: ID of the todo to update
            title: New title (optional)
            description: New description (optional)
            status: New status (optional)
            priority: New priority (optional)

        Returns:
            Todo: Updated todo if successful, None if todo doesn't exist
        """
        pass

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo by its ID.

        Args:
            todo_id: ID of the todo to delete

        Returns:
            bool: True if deletion successful, False if todo doesn't exist
        """
        pass

    def mark_complete(self, todo_id: int) -> Optional[Todo]:
        """
        Mark a todo as completed by setting its status to 'completed'.

        Args:
            todo_id: ID of the todo to mark as complete

        Returns:
            Todo: Updated todo if successful, None if todo doesn't exist
        """
        pass

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new todo.

        Returns:
            int: The next ID to be used (never reused after deletion)
        """
        pass
```

## Storage Contract

### In-Memory Storage
- **Type**: `Dict[int, Todo]` - dictionary mapping todo IDs to Todo objects
- **ID Counter**: Integer starting at 1, incremented for each new todo, never reused after deletion
- **Thread Safety**: Not required (single-threaded application)

## Validation Contract

### Input Validation
- **Title**: Required, 1-100 characters, non-empty
- **Description**: Optional, max 500 characters
- **Status**: Must be one of "pending", "in_progress", "completed"
- **Priority**: Must be one of "low", "medium", "high"
- **ID**: Auto-generated, unique, sequential

## Error Handling Contract

### Expected Exceptions
- `ValueError`: For invalid input parameters
- No unhandled exceptions should propagate to UI layer

### Error Messages
- All error messages should be user-friendly and provide guidance
- No stack traces to end user
- Clear indication of what went wrong and how to fix it

## Performance Contract

### Response Times
- All operations should complete in <100ms
- Startup time <1 second
- Memory usage <50MB for 1000 todos

## State Management Contract

### Session Scope
- All data lost on application exit
- Data persists only within current session
- No cross-session data sharing