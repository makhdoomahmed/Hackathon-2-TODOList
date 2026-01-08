#!/usr/bin/env python3
"""
Test script for User Story 2 - Update Todo Status functionality.
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'todo_app'))

from todo_app.src.service import TodoService
from todo_app.src.models import TodoPriority, TodoStatus


def test_mark_complete():
    """Test mark complete functionality."""
    print("Testing mark complete functionality...")

    # Create a service instance
    service = TodoService()

    # Add a todo
    todo = service.add_todo(
        title="Test Todo for Completion",
        description="This is a test todo to mark as complete",
        priority=TodoPriority.HIGH
    )

    print(f"✓ Created todo with ID: {todo.id}, Status: {todo.status}")

    # Verify initial status is pending
    if todo.status != TodoStatus.PENDING:
        print(f"✗ Expected status {TodoStatus.PENDING}, got {todo.status}")
        return False

    # Mark the todo as complete
    marked_todo = service.mark_complete(todo.id)

    if marked_todo is None:
        print("✗ Failed to mark todo as complete - todo not found")
        return False

    if marked_todo.status != TodoStatus.COMPLETED:
        print(f"✗ Expected status {TodoStatus.COMPLETED} after marking complete, got {marked_todo.status}")
        return False

    print(f"✓ Successfully marked todo as complete, new status: {marked_todo.status}")

    # Try to mark a non-existent todo
    result = service.mark_complete(999)
    if result is not None:
        print("✗ Should have returned None for non-existent todo ID")
        return False

    print("✓ Correctly handled non-existent todo ID")

    print("\n✓ All mark complete tests passed!")
    return True


def test_update_status():
    """Test update status functionality."""
    print("\nTesting update status functionality...")

    # Create a service instance
    service = TodoService()

    # Add a todo
    todo = service.add_todo(
        title="Test Todo for Status Update",
        description="This is a test todo to update status",
        priority=TodoPriority.MEDIUM
    )

    print(f"✓ Created todo with ID: {todo.id}, Status: {todo.status}")

    # Update the status to in_progress
    updated_todo = service.update_todo(todo.id, status=TodoStatus.IN_PROGRESS)

    if updated_todo is None:
        print("✗ Failed to update todo status - todo not found")
        return False

    if updated_todo.status != TodoStatus.IN_PROGRESS:
        print(f"✗ Expected status {TodoStatus.IN_PROGRESS}, got {updated_todo.status}")
        return False

    print(f"✓ Successfully updated status to: {updated_todo.status}")

    # Update the status to completed
    updated_todo2 = service.update_todo(todo.id, status=TodoStatus.COMPLETED)

    if updated_todo2.status != TodoStatus.COMPLETED:
        print(f"✗ Expected status {TodoStatus.COMPLETED}, got {updated_todo2.status}")
        return False

    print(f"✓ Successfully updated status to: {updated_todo2.status}")

    # Try to update status of non-existent todo
    result = service.update_todo(999, status=TodoStatus.PENDING)
    if result is not None:
        print("✗ Should have returned None for non-existent todo ID")
        return False

    print("✓ Correctly handled non-existent todo ID")

    print("\n✓ All update status tests passed!")
    return True


def test_validation_in_updates():
    """Test validation in update operations."""
    print("\nTesting validation in update operations...")

    service = TodoService()

    # Add a todo
    todo = service.add_todo(
        title="Test Todo for Validation",
        description="This is a test todo",
        priority=TodoPriority.LOW
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

    print("\n✓ All validation tests passed!")
    return True


if __name__ == "__main__":
    print("Running User Story 2 functionality tests for Todo Application...")

    success1 = test_mark_complete()
    success2 = test_update_status()
    success3 = test_validation_in_updates()

    if success1 and success2 and success3:
        print("\n🎉 All US2 tests passed! Mark Complete and Update Status functionality is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some US2 tests failed.")
        sys.exit(1)