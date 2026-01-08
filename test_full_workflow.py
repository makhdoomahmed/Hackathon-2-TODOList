#!/usr/bin/env python3
"""
Test script to verify the full application workflow: create → view → update → delete → exit
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'todo_app'))

from todo_app.src.service import TodoService
from todo_app.src.ui import TodoUI
from todo_app.src.models import TodoPriority, TodoStatus


def test_full_workflow():
    """Test the full application workflow."""
    print("Testing full application workflow: create → view → update → delete → exit")

    # Create service and UI instances
    service = TodoService()
    ui = TodoUI(service)

    print("\n1. Testing CREATE functionality...")
    # Test creating a todo
    # We'll simulate this directly since UI input mocking is complex
    todo = service.add_todo("Test Todo for Workflow", "This is a test todo for full workflow", TodoPriority.MEDIUM)
    print(f"✓ Created todo with ID: {todo.id}, Title: '{todo.title}', Status: {todo.status}")

    # Verify it was created
    all_todos = service.get_all_todos()
    if len(all_todos) == 1 and all_todos[0].id == 1:
        print("✓ Todo successfully stored in service layer")
    else:
        print("✗ Todo was not properly stored")
        return False

    print("\n2. Testing VIEW functionality...")
    # Test viewing todos
    view_result = service.get_all_todos()
    if len(view_result) == 1:
        print(f"✓ Successfully retrieved {len(view_result)} todo(s)")
        print(f"  - ID: {view_result[0].id}, Title: '{view_result[0].title}', Status: {view_result[0].status}")
    else:
        print("✗ Failed to retrieve todos")
        return False

    print("\n3. Testing UPDATE functionality...")
    # Test updating the todo
    updated_todo = service.update_todo(
        todo_id=todo.id,
        title="Updated Test Todo for Workflow",
        description="Updated description for workflow test",
        priority=TodoPriority.HIGH,
        status=TodoStatus.IN_PROGRESS
    )

    if updated_todo and updated_todo.title == "Updated Test Todo for Workflow":
        print(f"✓ Todo successfully updated - New title: '{updated_todo.title}', Status: {updated_todo.status}, Priority: {updated_todo.priority}")
    else:
        print("✗ Todo update failed")
        return False

    # Verify the update in storage
    retrieved_todo = service.get_todo_by_id(todo.id)
    if retrieved_todo and retrieved_todo.title == "Updated Test Todo for Workflow":
        print("✓ Update properly reflected in storage")
    else:
        print("✗ Update not properly reflected in storage")
        return False

    print("\n4. Testing MARK COMPLETE functionality...")
    # Test marking complete
    completed_todo = service.mark_complete(todo.id)
    if completed_todo and completed_todo.status == TodoStatus.COMPLETED:
        print(f"✓ Todo successfully marked as complete - Status: {completed_todo.status}")
    else:
        print("✗ Todo mark complete failed")
        return False

    print("\n5. Testing DELETE functionality...")
    # Test deleting the todo
    delete_success = service.delete_todo(todo.id)
    if delete_success:
        print("✓ Todo successfully deleted")
    else:
        print("✗ Todo deletion failed")
        return False

    # Verify deletion
    remaining_todos = service.get_all_todos()
    if len(remaining_todos) == 0:
        print("✓ Todo properly removed from storage")
    else:
        print("✗ Todo was not properly removed from storage")
        return False

    print("\n6. Testing multiple operations in sequence...")
    # Add multiple todos and test operations
    todo1 = service.add_todo("Workflow Test 1", "First test todo", TodoPriority.LOW)
    todo2 = service.add_todo("Workflow Test 2", "Second test todo", TodoPriority.HIGH)

    print(f"✓ Added two todos with IDs: {todo1.id} and {todo2.id}")

    # Update one
    updated = service.update_todo(todo1.id, title="Updated Workflow Test 1")
    if updated and updated.title == "Updated Workflow Test 1":
        print("✓ Multiple operations - update successful")
    else:
        print("✗ Multiple operations - update failed")
        return False

    # Mark one complete
    completed = service.mark_complete(todo2.id)
    if completed and completed.status == TodoStatus.COMPLETED:
        print("✓ Multiple operations - mark complete successful")
    else:
        print("✗ Multiple operations - mark complete failed")
        return False

    # View all
    all_todos = service.get_all_todos()
    if len(all_todos) == 2:
        print(f"✓ Multiple operations - view all shows {len(all_todos)} todos")
    else:
        print("✗ Multiple operations - view all failed")
        return False

    # Delete one
    delete_success = service.delete_todo(todo1.id)
    if delete_success:
        print("✓ Multiple operations - delete successful")
    else:
        print("✗ Multiple operations - delete failed")
        return False

    # Final view
    final_todos = service.get_all_todos()
    if len(final_todos) == 1 and final_todos[0].id == todo2.id:
        print("✓ Multiple operations - final state correct")
    else:
        print("✗ Multiple operations - final state incorrect")
        return False

    print("\n✅ All workflow tests passed!")
    return True


def test_error_conditions():
    """Test error conditions and edge cases."""
    print("\n\nTesting error conditions and edge cases...")

    service = TodoService()

    # Test non-existent ID operations
    print("\n1. Testing non-existent ID operations...")

    # Get non-existent
    result = service.get_todo_by_id(999)
    if result is None:
        print("✓ Non-existent ID correctly handled in get_todo_by_id")
    else:
        print("✗ Non-existent ID not handled in get_todo_by_id")
        return False

    # Update non-existent
    result = service.update_todo(999, title="Should not work")
    if result is None:
        print("✓ Non-existent ID correctly handled in update_todo")
    else:
        print("✗ Non-existent ID not handled in update_todo")
        return False

    # Delete non-existent
    result = service.delete_todo(999)
    if result is False:
        print("✓ Non-existent ID correctly handled in delete_todo")
    else:
        print("✗ Non-existent ID not handled in delete_todo")
        return False

    # Mark complete non-existent
    result = service.mark_complete(999)
    if result is None:
        print("✓ Non-existent ID correctly handled in mark_complete")
    else:
        print("✗ Non-existent ID not handled in mark_complete")
        return False

    print("\n2. Testing validation...")

    # Test empty title validation
    try:
        service.add_todo("", "Description", TodoPriority.HIGH)
        print("✗ Empty title should have been rejected in add_todo")
        return False
    except ValueError as e:
        if "Title is required" in str(e):
            print("✓ Empty title correctly rejected in add_todo")
        else:
            print(f"✗ Wrong error for empty title: {e}")
            return False

    # Test long title validation
    try:
        service.add_todo("A" * 101, "Description", TodoPriority.HIGH)
        print("✗ Long title should have been rejected in add_todo")
        return False
    except ValueError as e:
        if "Title must not exceed 100 characters" in str(e):
            print("✓ Long title correctly rejected in add_todo")
        else:
            print(f"✗ Wrong error for long title: {e}")
            return False

    # Add a todo to test update validation
    todo = service.add_todo("Valid Todo", "Description", TodoPriority.MEDIUM)

    # Test empty title in update
    try:
        service.update_todo(todo.id, title="")
        print("✗ Empty title should have been rejected in update_todo")
        return False
    except ValueError as e:
        if "Title is required" in str(e):
            print("✓ Empty title correctly rejected in update_todo")
        else:
            print(f"✗ Wrong error for empty title in update: {e}")
            return False

    # Test long title in update
    try:
        service.update_todo(todo.id, title="A" * 101)
        print("✗ Long title should have been rejected in update_todo")
        return False
    except ValueError as e:
        if "Title must not exceed 100 characters" in str(e):
            print("✓ Long title correctly rejected in update_todo")
        else:
            print(f"✗ Wrong error for long title in update: {e}")
            return False

    print("\n✅ All error condition tests passed!")
    return True


if __name__ == "__main__":
    print("Running full application workflow tests...")

    success1 = test_full_workflow()
    success2 = test_error_conditions()

    if success1 and success2:
        print("\n🎉 All full workflow tests passed! Application workflow is working correctly.")
        sys.exit(0)
    else:
        print("\n❌ Some full workflow tests failed.")
        sys.exit(1)