#!/usr/bin/env python3
"""
Test script for User Story 3 - Modify and Delete Todos functionality.
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'todo_app'))

from todo_app.src.service import TodoService
from todo_app.src.models import TodoPriority, TodoStatus


def test_delete_functionality():
    """Test delete functionality."""
    print("Testing delete functionality...")

    # Create a service instance
    service = TodoService()

    # Add a todo
    todo = service.add_todo(
        title="Test Todo for Deletion",
        description="This is a test todo to delete",
        priority=TodoPriority.HIGH
    )

    print(f"✓ Created todo with ID: {todo.id}")

    # Verify the todo exists
    retrieved_todo = service.get_todo_by_id(todo.id)
    if retrieved_todo is None:
        print("✗ Todo was not found after creation")
        return False

    # Count todos before deletion
    todos_before = len(service.get_all_todos())

    # Delete the todo
    success = service.delete_todo(todo.id)

    if not success:
        print("✗ Failed to delete todo")
        return False

    # Verify the todo no longer exists
    retrieved_todo_after = service.get_todo_by_id(todo.id)
    if retrieved_todo_after is not None:
        print("✗ Todo still exists after deletion")
        return False

    # Count todos after deletion
    todos_after = len(service.get_todo_by_id(todo.id)) if service.get_todo_by_id(todo.id) else len(service.get_all_todos())
    # Actually, let me recount properly
    todos_after = len(service.get_all_todos())

    if todos_after != todos_before - 1:
        print(f"✗ Expected {todos_before - 1} todos after deletion, got {todos_after}")
        return False

    print("✓ Successfully deleted todo and verified it no longer exists")

    # Try to delete a non-existent todo
    success_nonexistent = service.delete_todo(999)
    if success_nonexistent:
        print("✗ Should have returned False for non-existent todo ID")
        return False

    print("✓ Correctly handled non-existent todo ID")

    print("\n✓ All delete tests passed!")
    return True


def test_full_update_functionality():
    """Test full update functionality."""
    print("\nTesting full update functionality...")

    # Create a service instance
    service = TodoService()

    # Add a todo
    original_todo = service.add_todo(
        title="Original Title",
        description="Original Description",
        priority=TodoPriority.LOW
    )

    print(f"✓ Created todo with ID: {original_todo.id}")

    # Update multiple fields
    updated_todo = service.update_todo(
        todo_id=original_todo.id,
        title="Updated Title",
        description="Updated Description",
        priority=TodoPriority.HIGH,
        status=TodoStatus.IN_PROGRESS
    )

    if updated_todo is None:
        print("✗ Failed to update todo - todo not found")
        return False

    # Verify all fields were updated correctly
    if updated_todo.title != "Updated Title":
        print(f"✗ Title not updated correctly. Expected 'Updated Title', got '{updated_todo.title}'")
        return False

    if updated_todo.description != "Updated Description":
        print(f"✗ Description not updated correctly. Expected 'Updated Description', got '{updated_todo.description}'")
        return False

    if updated_todo.priority != TodoPriority.HIGH:
        print(f"✗ Priority not updated correctly. Expected {TodoPriority.HIGH}, got {updated_todo.priority}")
        return False

    if updated_todo.status != TodoStatus.IN_PROGRESS:
        print(f"✗ Status not updated correctly. Expected {TodoStatus.IN_PROGRESS}, got {updated_todo.status}")
        return False

    # Verify ID and creation time stayed the same
    if updated_todo.id != original_todo.id:
        print(f"✗ ID changed during update. Expected {original_todo.id}, got {updated_todo.id}")
        return False

    if updated_todo.created_at != original_todo.created_at:
        print(f"✗ Creation time changed during update")
        return False

    print("✓ Successfully updated all fields: title, description, priority, and status")

    # Test partial updates
    partial_updated = service.update_todo(
        todo_id=updated_todo.id,
        title="Partially Updated Title"
    )

    if partial_updated is None:
        print("✗ Failed partial update - todo not found")
        return False

    if partial_updated.title != "Partially Updated Title":
        print(f"✗ Title not updated in partial update. Expected 'Partially Updated Title', got '{partial_updated.title}'")
        return False

    # Description, priority, and status should remain as updated in previous step
    if partial_updated.description != "Updated Description":
        print(f"✗ Description changed in partial update. Expected 'Updated Description', got '{partial_updated.description}'")
        return False

    if partial_updated.priority != TodoPriority.HIGH:
        print(f"✗ Priority changed in partial update. Expected {TodoPriority.HIGH}, got {partial_updated.priority}")
        return False

    if partial_updated.status != TodoStatus.IN_PROGRESS:
        print(f"✗ Status changed in partial update. Expected {TodoStatus.IN_PROGRESS}, got {partial_updated.status}")
        return False

    print("✓ Successfully performed partial update - only title changed")

    # Try to update non-existent todo
    result = service.update_todo(999, title="Should not work")
    if result is not None:
        print("✗ Should have returned None for non-existent todo ID")
        return False

    print("✓ Correctly handled non-existent todo ID")

    print("\n✓ All full update tests passed!")
    return True


def test_update_validation():
    """Test validation in update operations."""
    print("\nTesting update validation...")

    service = TodoService()

    # Add a todo
    todo = service.add_todo(
        title="Test Todo for Validation",
        description="This is a test todo",
        priority=TodoPriority.MEDIUM
    )

    # Test updating with invalid title (empty)
    try:
        service.update_todo(todo.id, title="")
        print("✗ Should have raised ValueError for empty title")
        return False
    except ValueError as e:
        if "Title is required" in str(e):
            print("✓ Correctly validated empty title during update")
        else:
            print(f"✗ Wrong error message: {e}")
            return False

    # Test updating with invalid title (too long)
    try:
        long_title = "A" * 101  # 101 characters, exceeding 100
        service.update_todo(todo.id, title=long_title)
        print("✗ Should have raised ValueError for long title")
        return False
    except ValueError as e:
        if "Title must not exceed 100 characters" in str(e):
            print("✓ Correctly validated long title during update")
        else:
            print(f"✗ Wrong error message: {e}")
            return False

    # Test that original title remains unchanged after validation failures
    unchanged_todo = service.get_todo_by_id(todo.id)
    if unchanged_todo.title != "Test Todo for Validation":
        print(f"✗ Original title was changed despite validation error. Got: {unchanged_todo.title}")
        return False

    print("✓ Original title remained unchanged after validation errors")

    print("\n✓ All update validation tests passed!")
    return True


if __name__ == "__main__":
    print("Running User Story 3 functionality tests for Todo Application...")

    success1 = test_delete_functionality()
    success2 = test_full_update_functionality()
    success3 = test_update_validation()

    if success1 and success2 and success3:
        print("\n🎉 All US3 tests passed! Delete and Full Update functionality is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some US3 tests failed.")
        sys.exit(1)