#!/usr/bin/env python3
"""
Entry point for the Phase I In-Memory Python Console Todo Application.
"""

import sys
from .service import TodoService
from .ui import TodoUI


def main():
    """
    Main entry point for the application.
    Creates the service and UI instances and starts the application loop.
    """
    # Create service instance
    service = TodoService()

    # Create UI instance with the service
    ui = TodoUI(service)

    # Start the application
    try:
        ui.run()
    except KeyboardInterrupt:
        print("\nApplication terminated by user.")
        sys.exit(0)
    except Exception as e:
        print(f"An unexpected error occurred: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()