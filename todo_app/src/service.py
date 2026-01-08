from typing import List, Optional, Dict
from datetime import datetime
from .models import Todo, TodoStatus, TodoPriority


class TodoService:
    """
    TodoService class handles all business logic for the console todo application.

    Attributes:
        todos: Dictionary mapping todo IDs to Todo objects
        next_id: Integer counter for generating unique IDs
    """

    def __init__(self):
        """Initialize the service with empty storage and ID counter"""
        self.todos: Dict[int, Todo] = {}
        self.next_id: int = 1

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
        # Validate title
        if not title or len(title.strip()) == 0:
            raise ValueError("Title is required")
        if len(title) > 100:
            raise ValueError("Title must not exceed 100 characters")

        # Create new todo with current ID and increment counter
        todo_id = self.next_id
        self.next_id += 1

        new_todo = Todo(
            id=todo_id,
            title=title.strip(),
            description=description,
            priority=priority,
            created_at=datetime.now()
        )

        # Add to storage
        self.todos[todo_id] = new_todo

        return new_todo

    def get_all_todos(self) -> List[Todo]:
        """
        Retrieve all todos sorted by ID.

        Returns:
            List[Todo]: All todos in the system, sorted by ID
        """
        # Return all todos sorted by ID
        return sorted(self.todos.values(), key=lambda x: x.id)

    def get_todo_by_id(self, todo_id: int) -> Optional[Todo]:
        """
        Retrieve a specific todo by its ID.

        Args:
            todo_id: The ID of the todo to retrieve

        Returns:
            Todo: The todo if found, None otherwise
        """
        return self.todos.get(todo_id)

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
        if todo_id not in self.todos:
            return None

        todo = self.todos[todo_id]

        # Validate title if provided
        if title is not None:
            if not title or len(title.strip()) == 0:
                raise ValueError("Title is required")
            if len(title) > 100:
                raise ValueError("Title must not exceed 100 characters")

        # Prepare updated values
        updated_id = todo.id
        updated_title = title.strip() if title is not None else todo.title
        updated_description = description if description is not None else todo.description
        updated_status = status if status is not None else todo.status
        updated_priority = priority if priority is not None else todo.priority
        updated_created_at = todo.created_at

        # Create updated todo
        updated_todo = Todo(
            id=updated_id,
            title=updated_title,
            description=updated_description,
            status=updated_status,
            priority=updated_priority,
            created_at=updated_created_at
        )

        # Update storage
        self.todos[todo_id] = updated_todo
        return updated_todo

    def delete_todo(self, todo_id: int) -> bool:
        """
        Delete a todo by its ID.

        Args:
            todo_id: ID of the todo to delete

        Returns:
            bool: True if deletion successful, False if todo doesn't exist
        """
        if todo_id not in self.todos:
            return False

        del self.todos[todo_id]
        return True

    def mark_complete(self, todo_id: int) -> Optional[Todo]:
        """
        Mark a todo as completed by setting its status to 'completed'.

        Args:
            todo_id: ID of the todo to mark as complete

        Returns:
            Todo: Updated todo if successful, None if todo doesn't exist
        """
        if todo_id not in self.todos:
            return None

        todo = self.todos[todo_id]
        updated_todo = Todo(
            id=todo.id,
            title=todo.title,
            description=todo.description,
            status=TodoStatus.COMPLETED,
            priority=todo.priority,
            created_at=todo.created_at
        )

        self.todos[todo_id] = updated_todo
        return updated_todo

    def get_next_id(self) -> int:
        """
        Get the next available ID for a new todo.

        Returns:
            int: The next ID to be used (never reused after deletion)
        """
        return self.next_id