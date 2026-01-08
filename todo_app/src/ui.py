from typing import Optional
from .models import Todo, TodoStatus, TodoPriority
from .service import TodoService


class TodoUI:
    """
    TodoUI class handles all console interface for the todo application.

    Attributes:
        service: TodoService instance for business logic
    """

    def __init__(self, service: TodoService):
        """
        Initialize the UI with a TodoService instance.

        Args:
            service: TodoService instance for business logic
        """
        self.service = service

    def display_menu(self):
        """Display the main menu with numbered options for all 6 operations."""
        print("\n" + "="*40)
        print("         TODO APPLICATION MENU")
        print("="*40)
        print("1. Add Todo")
        print("2. View Todos")
        print("3. Update Todo")
        print("4. Delete Todo")
        print("5. Mark Complete")
        print("6. Exit")
        print("="*40)

    def get_user_choice(self) -> int:
        """
        Get user's menu choice with validation.

        Returns:
            int: User's menu choice (1-6) or -1 for invalid input
        """
        try:
            choice = input("\nEnter your choice (1-6): ").strip()

            if not choice.isdigit():
                return -1

            choice_int = int(choice)
            if 1 <= choice_int <= 6:
                return choice_int
            else:
                return -1
        except:
            return -1

    def create_todo(self):
        """Implement create todo functionality in UI layer with input prompts and validation."""
        try:
            # Get title with validation
            print("Creating a new todo...")
            title_input = input("Enter title (required, max 100 characters): ").strip()

            if not title_input:
                self.display_error("Title is required")
                return
            if len(title_input) > 100:
                self.display_error("Title must not exceed 100 characters")
                return

            # Get description (optional)
            description_input = input("Enter description (optional, max 500 characters): ").strip()
            if not description_input:
                description_input = None

            # Get priority with validation
            print("Select priority:")
            print("1. Low")
            print("2. Medium")
            print("3. High")

            priority_choice = input("Enter priority (1-3): ").strip()
            priority_map = {"1": TodoPriority.LOW, "2": TodoPriority.MEDIUM, "3": TodoPriority.HIGH}

            if priority_choice not in priority_map:
                self.display_error("Invalid priority. Please enter 1, 2, or 3.")
                return

            priority = priority_map[priority_choice]

            # Create the todo
            todo = self.service.add_todo(title_input, description_input, priority)
            print(f"Todo created successfully with ID: {todo.id}")

        except ValueError as e:
            self.display_error(str(e))
        except Exception as e:
            self.display_error(f"Error creating todo: {str(e)}")

    def view_todos(self):
        """Implement view todos functionality in UI layer with table-like display format."""
        try:
            todos = self.service.get_all_todos()

            if not todos:
                print("No todos found")
                return

            # Display todos in a table-like format
            self.display_todo_table(todos)

        except Exception as e:
            self.display_error(f"Error viewing todos: {str(e)}")

    def update_todo(self):
        """Implement update todo functionality in UI layer for status changes and all attributes."""
        try:
            # Get the todo ID from user
            id_input = input("Enter the ID of the todo to update: ").strip()

            if not id_input.isdigit():
                self.display_error("Invalid ID. Please enter a numeric value.")
                return

            todo_id = int(id_input)

            # Check if the todo exists
            todo = self.service.get_todo_by_id(todo_id)
            if todo is None:
                self.display_error(f"Todo with ID {todo_id} not found.")
                return

            print(f"Updating todo ID {todo_id}: {todo.title}")

            # Ask what to update
            print("\nWhat would you like to update?")
            print("1. Title")
            print("2. Description")
            print("3. Priority")
            print("4. Status")
            print("5. Multiple fields")
            print("6. Cancel")

            choice = input("Enter your choice (1-6): ").strip()

            # Prepare update parameters
            title = None
            description = None
            priority = None
            status = None

            if choice == "1":
                # Update title only
                new_title = input(f"Enter new title (current: '{todo.title}', press Enter to keep current): ").strip()
                if new_title:
                    title = new_title
                else:
                    title = todo.title
            elif choice == "2":
                # Update description only
                new_desc = input(f"Enter new description (current: '{todo.description or ''}', press Enter to keep current): ").strip()
                if new_desc != "":
                    description = new_desc if new_desc else None
                else:
                    description = todo.description
            elif choice == "3":
                # Update priority only
                print("Select new priority:")
                print("1. Low")
                print("2. Medium")
                print("3. High")
                priority_choice = input("Enter priority (1-3): ").strip()
                priority_map = {"1": TodoPriority.LOW, "2": TodoPriority.MEDIUM, "3": TodoPriority.HIGH}

                if priority_choice in priority_map:
                    priority = priority_map[priority_choice]
                else:
                    self.display_error("Invalid priority selection.")
                    return
            elif choice == "4":
                # Update status only
                print("Select new status:")
                print("1. Pending")
                print("2. In Progress")
                print("3. Completed")
                status_choice = input("Enter status (1-3): ").strip()
                status_map = {"1": TodoStatus.PENDING, "2": TodoStatus.IN_PROGRESS, "3": TodoStatus.COMPLETED}

                if status_choice in status_map:
                    status = status_map[status_choice]
                else:
                    self.display_error("Invalid status selection.")
                    return
            elif choice == "5":
                # Update multiple fields
                new_title = input(f"Enter new title (current: '{todo.title}', press Enter to keep current): ").strip()
                if new_title:
                    title = new_title

                new_desc = input(f"Enter new description (current: '{todo.description or ''}', press Enter to keep current): ").strip()
                if new_desc != "":
                    description = new_desc if new_desc else None

                print("Select new priority (press Enter to keep current):")
                print("1. Low")
                print("2. Medium")
                print("3. High")
                priority_choice = input("Enter priority (1-3, or Enter to skip): ").strip()
                priority_map = {"1": TodoPriority.LOW, "2": TodoPriority.MEDIUM, "3": TodoPriority.HIGH}

                if priority_choice in priority_map:
                    priority = priority_map[priority_choice]
                elif priority_choice != "":
                    self.display_error("Invalid priority selection.")
                    return

                print("Select new status (press Enter to keep current):")
                print("1. Pending")
                print("2. In Progress")
                print("3. Completed")
                status_choice = input("Enter status (1-3, or Enter to skip): ").strip()
                status_map = {"1": TodoStatus.PENDING, "2": TodoStatus.IN_PROGRESS, "3": TodoStatus.COMPLETED}

                if status_choice in status_map:
                    status = status_map[status_choice]
                elif status_choice != "":
                    self.display_error("Invalid status selection.")
                    return
            elif choice == "6":
                print("Update canceled.")
                return
            else:
                self.display_error("Invalid choice.")
                return

            # Perform the update
            updated_todo = self.service.update_todo(
                todo_id=todo_id,
                title=title,
                description=description,
                priority=priority,
                status=status
            )

            if updated_todo is not None:
                print(f"Todo ID {todo_id} updated successfully!")
            else:
                self.display_error(f"Failed to update todo ID {todo_id}.")

        except ValueError as e:
            self.display_error(str(e))
        except Exception as e:
            self.display_error(f"Error updating todo: {str(e)}")

    def delete_todo(self):
        """Implement delete todo functionality in UI layer with ID input and validation."""
        try:
            # Get the todo ID from user
            id_input = input("Enter the ID of the todo to delete: ").strip()

            if not id_input.isdigit():
                self.display_error("Invalid ID. Please enter a numeric value.")
                return

            todo_id = int(id_input)

            # Confirm deletion
            todo = self.service.get_todo_by_id(todo_id)
            if todo is None:
                self.display_error(f"Todo with ID {todo_id} not found.")
                return

            print(f"You are about to delete: {todo.title}")
            confirm = input("Are you sure you want to delete this todo? (y/N): ").strip().lower()

            if confirm not in ['y', 'yes']:
                print("Deletion canceled.")
                return

            # Attempt to delete the todo
            success = self.service.delete_todo(todo_id)

            if success:
                print(f"Todo ID {todo_id} deleted successfully!")
            else:
                self.display_error(f"Failed to delete todo with ID {todo_id}.")

        except Exception as e:
            self.display_error(f"Error deleting todo: {str(e)}")

    def mark_complete(self):
        """Implement mark complete functionality in UI layer with ID input and validation."""
        try:
            # Get the todo ID from user
            id_input = input("Enter the ID of the todo to mark as complete: ").strip()

            if not id_input.isdigit():
                self.display_error("Invalid ID. Please enter a numeric value.")
                return

            todo_id = int(id_input)

            # Attempt to mark the todo as complete
            result = self.service.mark_complete(todo_id)

            if result is not None:
                print(f"Todo ID {todo_id} marked as complete successfully!")
            else:
                self.display_error(f"Todo with ID {todo_id} not found.")

        except ValueError as e:
            self.display_error(str(e))
        except Exception as e:
            self.display_error(f"Error marking todo as complete: {str(e)}")

    def run(self):
        """Main UI loop that continues until user chooses to exit."""
        while True:
            try:
                self.display_menu()
                choice = self.get_user_choice()

                if choice == 1:
                    self.create_todo()
                elif choice == 2:
                    self.view_todos()
                elif choice == 3:
                    self.update_todo()
                elif choice == 4:
                    self.delete_todo()
                elif choice == 5:
                    self.mark_complete()
                elif choice == 6:
                    print("Goodbye!")
                    break
                else:
                    print("Invalid option. Please try again.")

                # Return to main menu after each operation
                input("\nPress Enter to continue...")

            except KeyboardInterrupt:
                print("\nApplication terminated by user.")
                break
            except Exception as e:
                print(f"An unexpected error occurred: {e}")
                input("\nPress Enter to continue...")

    def display_todo_table(self, todos: list):
        """Display todos in a table-like format."""
        # Print table header
        print("\n" + "="*80)
        print(f"{'ID':<5} {'Title':<20} {'Status':<12} {'Priority':<10} {'Created At':<20}")
        print("="*80)

        # Print each todo
        for todo in todos:
            title = todo.title[:17] + "..." if len(todo.title) > 20 else todo.title
            created_at_str = todo.created_at.strftime("%Y-%m-%d %H:%M")
            print(f"{todo.id:<5} {title:<20} {todo.status.value:<12} {todo.priority.value:<10} {created_at_str:<20}")

        print("="*80 + "\n")

    def get_valid_title(self) -> Optional[str]:
        """
        Get a valid title from user with validation.

        Returns:
            str: Valid title or None if user cancels
        """
        pass

    def get_valid_description(self) -> Optional[str]:
        """
        Get a valid description from user.

        Returns:
            str: Valid description or None
        """
        pass

    def get_valid_priority(self) -> Optional[TodoPriority]:
        """
        Get a valid priority from user with validation.

        Returns:
            TodoPriority: Valid priority or None if user cancels
        """
        pass

    def get_todo_id(self) -> Optional[int]:
        """
        Get a valid todo ID from user.

        Returns:
            int: Valid todo ID or None if user cancels
        """
        pass

    def display_message(self, message: str):
        """
        Display a message to the user.

        Args:
            message: Message to display
        """
        print(message)

    def display_error(self, error: str):
        """
        Display an error message to the user with guidance.

        Args:
            error: Error message to display
        """
        print(f"Error: {error}")