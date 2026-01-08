import pytest
import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from service import TodoService
from models import TodoPriority, TodoStatus


class TestTodoService:
    """Unit tests for TodoService class."""

    def setup_method(self):
        """Set up a fresh TodoService instance for each test."""
        self.service = TodoService()

    def test_add_todo_success(self):
        """Test successful addition of a todo."""
        todo = self.service.add_todo(
            title="Test Todo",
            description="Test Description",
            priority=TodoPriority.HIGH
        )

        assert todo.title == "Test Todo"
        assert todo.description == "Test Description"
        assert todo.priority == TodoPriority.HIGH
        assert todo.status == TodoStatus.PENDING  # Default status
        assert todo.id == 1  # First todo gets ID 1

        # Verify todo is stored
        stored_todo = self.service.get_todo_by_id(1)
        assert stored_todo is not None
        assert stored_todo.id == todo.id

    def test_add_todo_validation_title_required(self):
        """Test that adding a todo with empty title raises ValueError."""
        with pytest.raises(ValueError, match="Title is required"):
            self.service.add_todo("", "Description", TodoPriority.HIGH)

        with pytest.raises(ValueError, match="Title is required"):
            self.service.add_todo("   ", "Description", TodoPriority.HIGH)  # Whitespace only

    def test_add_todo_validation_title_length(self):
        """Test that adding a todo with title exceeding 100 characters raises ValueError."""
        long_title = "A" * 101  # 101 characters

        with pytest.raises(ValueError, match="Title must not exceed 100 characters"):
            self.service.add_todo(long_title, "Description", TodoPriority.HIGH)

    def test_get_all_todos_empty(self):
        """Test getting all todos when list is empty."""
        todos = self.service.get_all_todos()
        assert len(todos) == 0

    def test_get_all_todos_with_items(self):
        """Test getting all todos when list has items."""
        # Add multiple todos
        todo1 = self.service.add_todo("Todo 1", "Description 1", TodoPriority.LOW)
        todo2 = self.service.add_todo("Todo 2", "Description 2", TodoPriority.MEDIUM)
        todo3 = self.service.add_todo("Todo 3", "Description 3", TodoPriority.HIGH)

        todos = self.service.get_all_todos()

        assert len(todos) == 3
        # Verify they are sorted by ID
        assert todos[0].id == 1
        assert todos[1].id == 2
        assert todos[2].id == 3

    def test_get_todo_by_id_found(self):
        """Test getting a todo by ID when it exists."""
        added_todo = self.service.add_todo("Test Todo", "Description", TodoPriority.HIGH)

        retrieved_todo = self.service.get_todo_by_id(added_todo.id)

        assert retrieved_todo is not None
        assert retrieved_todo.id == added_todo.id
        assert retrieved_todo.title == added_todo.title
        assert retrieved_todo.description == added_todo.description

    def test_get_todo_by_id_not_found(self):
        """Test getting a todo by ID when it doesn't exist."""
        result = self.service.get_todo_by_id(999)
        assert result is None

    def test_update_todo_success(self):
        """Test successful update of a todo."""
        original_todo = self.service.add_todo("Original Title", "Original Description", TodoPriority.LOW)

        updated_todo = self.service.update_todo(
            todo_id=original_todo.id,
            title="Updated Title",
            description="Updated Description",
            priority=TodoPriority.HIGH,
            status=TodoStatus.IN_PROGRESS
        )

        assert updated_todo is not None
        assert updated_todo.id == original_todo.id  # ID should not change
        assert updated_todo.title == "Updated Title"
        assert updated_todo.description == "Updated Description"
        assert updated_todo.priority == TodoPriority.HIGH
        assert updated_todo.status == TodoStatus.IN_PROGRESS

    def test_update_todo_partial(self):
        """Test partial update of a todo (only some fields)."""
        original_todo = self.service.add_todo("Original Title", "Original Description", TodoPriority.LOW)

        updated_todo = self.service.update_todo(
            todo_id=original_todo.id,
            title="Updated Title"
        )

        assert updated_todo is not None
        assert updated_todo.id == original_todo.id
        assert updated_todo.title == "Updated Title"  # Changed
        assert updated_todo.description == "Original Description"  # Unchanged
        assert updated_todo.priority == TodoPriority.LOW  # Unchanged
        assert updated_todo.status == TodoStatus.PENDING  # Unchanged (default)

    def test_update_todo_not_found(self):
        """Test updating a todo that doesn't exist."""
        result = self.service.update_todo(
            todo_id=999,
            title="Updated Title"
        )

        assert result is None

    def test_update_todo_validation(self):
        """Test validation in update operations."""
        original_todo = self.service.add_todo("Original Title", "Description", TodoPriority.HIGH)

        # Test updating with empty title
        with pytest.raises(ValueError, match="Title is required"):
            self.service.update_todo(original_todo.id, title="")

        # Test updating with long title
        with pytest.raises(ValueError, match="Title must not exceed 100 characters"):
            self.service.update_todo(original_todo.id, title="A" * 101)

    def test_delete_todo_success(self):
        """Test successful deletion of a todo."""
        todo = self.service.add_todo("Test Todo", "Description", TodoPriority.HIGH)

        # Verify todo exists before deletion
        assert self.service.get_todo_by_id(todo.id) is not None

        # Delete the todo
        success = self.service.delete_todo(todo.id)

        assert success is True
        # Verify todo no longer exists
        assert self.service.get_todo_by_id(todo.id) is None

    def test_delete_todo_not_found(self):
        """Test deleting a todo that doesn't exist."""
        success = self.service.delete_todo(999)
        assert success is False

    def test_mark_complete_success(self):
        """Test successful marking of a todo as complete."""
        todo = self.service.add_todo("Test Todo", "Description", TodoPriority.HIGH)

        marked_todo = self.service.mark_complete(todo.id)

        assert marked_todo is not None
        assert marked_todo.id == todo.id
        assert marked_todo.status == TodoStatus.COMPLETED

    def test_mark_complete_not_found(self):
        """Test marking complete on a todo that doesn't exist."""
        result = self.service.mark_complete(999)
        assert result is None

    def test_id_generation_sequential_no_reuse(self):
        """Test that IDs are generated sequentially and not reused after deletion."""
        # Add a few todos
        todo1 = self.service.add_todo("Todo 1", "Description 1", TodoPriority.LOW)
        todo2 = self.service.add_todo("Todo 2", "Description 2", TodoPriority.MEDIUM)
        todo3 = self.service.add_todo("Todo 3", "Description 3", TodoPriority.HIGH)

        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3

        # Delete the middle todo
        success = self.service.delete_todo(2)
        assert success is True

        # Add a new todo - it should get ID 4, not reuse ID 2
        todo4 = self.service.add_todo("Todo 4", "Description 4", TodoPriority.HIGH)

        assert todo4.id == 4

    def test_get_next_id(self):
        """Test that get_next_id returns the next available ID."""
        assert self.service.get_next_id() == 1

        self.service.add_todo("Todo 1", "Description", TodoPriority.HIGH)
        assert self.service.get_next_id() == 2

        self.service.add_todo("Todo 2", "Description", TodoPriority.HIGH)
        assert self.service.get_next_id() == 3


class TestTodoServiceEdgeCases:
    """Edge case tests for TodoService."""

    def setup_method(self):
        """Set up a fresh TodoService instance for each test."""
        self.service = TodoService()

    def test_multiple_operations_sequence(self):
        """Test a sequence of operations to ensure consistency."""
        # Add multiple todos
        todo1 = self.service.add_todo("Todo 1", "Description 1", TodoPriority.LOW)
        todo2 = self.service.add_todo("Todo 2", "Description 2", TodoPriority.MEDIUM)
        todo3 = self.service.add_todo("Todo 3", "Description 3", TodoPriority.HIGH)

        # Update one
        updated_todo = self.service.update_todo(todo2.id, title="Updated Todo 2")
        assert updated_todo.title == "Updated Todo 2"

        # Mark one complete
        completed_todo = self.service.mark_complete(todo1.id)
        assert completed_todo.status == TodoStatus.COMPLETED

        # Delete one
        success = self.service.delete_todo(todo3.id)
        assert success is True

        # Get all and verify state
        all_todos = self.service.get_all_todos()
        assert len(all_todos) == 2  # Two remaining (todo1 and todo2)

        # Verify specific todos
        retrieved_todo1 = self.service.get_todo_by_id(todo1.id)
        assert retrieved_todo1.status == TodoStatus.COMPLETED

        retrieved_todo2 = self.service.get_todo_by_id(todo2.id)
        assert retrieved_todo2.title == "Updated Todo 2"