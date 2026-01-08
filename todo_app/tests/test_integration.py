import pytest
import sys
import os
from unittest.mock import patch, MagicMock

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'src'))

from service import TodoService
from models import TodoPriority, TodoStatus
from ui import TodoUI


class TestIntegration:
    """Integration tests for the todo application."""

    def setup_method(self):
        """Set up a TodoService and TodoUI instance for each test."""
        self.service = TodoService()
        self.ui = TodoUI(self.service)

    @patch('builtins.input')
    @patch('builtins.print')
    def test_create_and_view_todo(self, mock_print, mock_input):
        """Test creating and viewing a todo through UI."""
        # Mock user inputs for creating a todo
        mock_input.side_effect = [
            "Test Title",  # title
            "Test Description",  # description
            "3",  # priority (HIGH)
            "y"  # confirm (for delete)
        ]

        # Test create todo
        self.ui.create_todo()

        # Verify a todo was created
        todos = self.service.get_all_todos()
        assert len(todos) == 1
        assert todos[0].title == "Test Title"
        assert todos[0].description == "Test Description"
        assert todos[0].priority == TodoPriority.HIGH

        # Test view todos
        self.ui.view_todos()
        # This should print the todo table

    def test_basic_crud_operations(self):
        """Test basic CRUD operations through service."""
        # Create
        todo = self.service.add_todo("Test Title", "Test Description", TodoPriority.MEDIUM)
        assert todo.title == "Test Title"
        assert todo.description == "Test Description"
        assert todo.priority == TodoPriority.MEDIUM

        # Read (get all)
        all_todos = self.service.get_all_todos()
        assert len(all_todos) == 1

        # Read (get by ID)
        retrieved_todo = self.service.get_todo_by_id(todo.id)
        assert retrieved_todo is not None
        assert retrieved_todo.title == "Test Title"

        # Update
        updated_todo = self.service.update_todo(
            todo_id=todo.id,
            title="Updated Title",
            status=TodoStatus.IN_PROGRESS
        )
        assert updated_todo.title == "Updated Title"
        assert updated_todo.status == TodoStatus.IN_PROGRESS

        # Mark complete
        completed_todo = self.service.mark_complete(todo.id)
        assert completed_todo.status == TodoStatus.COMPLETED

        # Delete
        result = self.service.delete_todo(todo.id)
        assert result is True

        # Verify deletion
        all_todos = self.service.get_all_todos()
        assert len(all_todos) == 0

    def test_todo_validation(self):
        """Test validation in todo operations."""
        # Test adding todo with empty title
        with pytest.raises(ValueError, match="Title is required"):
            self.service.add_todo("", "Description", TodoPriority.HIGH)

        # Test adding todo with long title
        with pytest.raises(ValueError, match="Title must not exceed 100 characters"):
            self.service.add_todo("A" * 101, "Description", TodoPriority.HIGH)

        # Test updating with empty title
        todo = self.service.add_todo("Valid Title", "Description", TodoPriority.LOW)
        with pytest.raises(ValueError, match="Title is required"):
            self.service.update_todo(todo.id, title="")

        # Test updating with long title
        with pytest.raises(ValueError, match="Title must not exceed 100 characters"):
            self.service.update_todo(todo.id, title="A" * 101)

    def test_nonexistent_id_operations(self):
        """Test operations with non-existent IDs."""
        # Test get by non-existent ID
        result = self.service.get_todo_by_id(999)
        assert result is None

        # Test update non-existent ID
        result = self.service.update_todo(999, title="New Title")
        assert result is None

        # Test delete non-existent ID
        result = self.service.delete_todo(999)
        assert result is False

        # Test mark complete non-existent ID
        result = self.service.mark_complete(999)
        assert result is None

    def test_id_generation_and_reuse(self):
        """Test ID generation and that IDs are not reused after deletion."""
        # Add multiple todos
        todo1 = self.service.add_todo("Todo 1", "Desc 1", TodoPriority.LOW)
        todo2 = self.service.add_todo("Todo 2", "Desc 2", TodoPriority.MEDIUM)
        todo3 = self.service.add_todo("Todo 3", "Desc 3", TodoPriority.HIGH)

        # Verify sequential IDs
        assert todo1.id == 1
        assert todo2.id == 2
        assert todo3.id == 3

        # Delete middle todo
        success = self.service.delete_todo(2)
        assert success is True

        # Add new todo - should get next available ID (4), not reuse 2
        todo4 = self.service.add_todo("Todo 4", "Desc 4", TodoPriority.HIGH)
        assert todo4.id == 4

    def test_enum_restrictions(self):
        """Test that only valid enum values are accepted."""
        # Test that we can create todos with valid priorities and statuses
        todo = self.service.add_todo("Test", "Description", TodoPriority.HIGH)
        assert todo.priority == TodoPriority.HIGH

        # Update with valid status
        updated = self.service.update_todo(todo.id, status=TodoStatus.IN_PROGRESS)
        assert updated.status == TodoStatus.IN_PROGRESS