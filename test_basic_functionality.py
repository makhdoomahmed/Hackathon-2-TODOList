#!/usr/bin/env python3
"""
Basic test script to verify the core functionality of the Todo application.
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'todo_app'))

from todo_app.src.service import TodoService
from todo_app.src.models import TodoPriority


def test_basic_functionality():
    """Test basic create and view functionality."""
    print("Testing basic functionality...")

    # Create a service instance
    service = TodoService()

    # Test 1: Add a todo
    print("\n1. Testing add_todo functionality...")
    try:
        todo1 = service.add_todo(
            title="Test Todo 1",
            description="This is a test todo",
            priority=TodoPriority.HIGH
        )
        print(f"✓ Successfully created todo with ID: {todo1.id}, Title: {todo1.title}")

        todo2 = service.add_todo(
            title="Test Todo 2",
            description="Another test todo",
            priority=TodoPriority.MEDIUM
        )
        print(f"✓ Successfully created todo with ID: {todo2.id}, Title: {todo2.title}")

    except Exception as e:
        print(f"✗ Failed to create todo: {e}")
        return False

    # Test 2: Get all todos
    print("\n2. Testing get_all_todos functionality...")
    try:
        all_todos = service.get_all_todos()
        print(f"✓ Retrieved {len(all_todos)} todos")
        for todo in all_todos:
            print(f"  - ID: {todo.id}, Title: {todo.title}, Status: {todo.status}, Priority: {todo.priority}")

        # Verify the todos are sorted by ID
        if len(all_todos) >= 2:
            if all_todos[0].id <= all_todos[1].id:
                print("✓ Todos are correctly sorted by ID")
            else:
                print("✗ Todos are not sorted by ID")
                return False

    except Exception as e:
        print(f"✗ Failed to retrieve todos: {e}")
        return False

    # Test 3: Add another todo and verify sorting
    print("\n3. Testing ID generation and sorting...")
    try:
        todo3 = service.add_todo(
            title="Test Todo 3",
            description="Third test todo",
            priority=TodoPriority.LOW
        )
        print(f"✓ Successfully created todo with ID: {todo3.id}, Title: {todo3.title}")

        all_todos = service.get_all_todos()
        print(f"✓ Now have {len(all_todos)} todos total")

        # Verify IDs are sequential and not reused
        expected_ids = [1, 2, 3]
        actual_ids = [t.id for t in all_todos]
        if actual_ids == expected_ids:
            print("✓ IDs are sequential and correctly assigned")
        else:
            print(f"✗ Expected IDs {expected_ids}, got {actual_ids}")
            return False

    except Exception as e:
        print(f"✗ Failed during ID generation test: {e}")
        return False

    print("\n✓ All basic functionality tests passed!")
    return True


def test_validation():
    """Test validation functionality."""
    print("\n\nTesting validation functionality...")

    service = TodoService()

    # Test 1: Empty title validation
    print("\n1. Testing empty title validation...")
    try:
        service.add_todo("", "Description", TodoPriority.HIGH)
        print("✗ Should have failed with empty title")
        return False
    except ValueError as e:
        if "Title is required" in str(e):
            print("✓ Correctly rejected empty title")
        else:
            print(f"✗ Wrong error message for empty title: {e}")
            return False
    except Exception as e:
        print(f"✗ Unexpected error for empty title: {e}")
        return False

    # Test 2: Whitespace-only title validation
    print("\n2. Testing whitespace-only title validation...")
    try:
        service.add_todo("   ", "Description", TodoPriority.HIGH)
        print("✗ Should have failed with whitespace-only title")
        return False
    except ValueError as e:
        if "Title is required" in str(e):
            print("✓ Correctly rejected whitespace-only title")
        else:
            print(f"✗ Wrong error message for whitespace-only title: {e}")
            return False
    except Exception as e:
        print(f"✗ Unexpected error for whitespace-only title: {e}")
        return False

    # Test 3: Too-long title validation
    print("\n3. Testing long title validation...")
    long_title = "A" * 101  # 101 characters, exceeding 100
    try:
        service.add_todo(long_title, "Description", TodoPriority.HIGH)
        print("✗ Should have failed with long title")
        return False
    except ValueError as e:
        if "Title must not exceed 100 characters" in str(e):
            print("✓ Correctly rejected long title")
        else:
            print(f"✗ Wrong error message for long title: {e}")
            return False
    except Exception as e:
        print(f"✗ Unexpected error for long title: {e}")
        return False

    print("\n✓ All validation tests passed!")
    return True


if __name__ == "__main__":
    print("Running basic functionality tests for Todo Application...")

    success1 = test_basic_functionality()
    success2 = test_validation()

    if success1 and success2:
        print("\n🎉 All tests passed! Basic functionality is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some tests failed.")
        sys.exit(1)