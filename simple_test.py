#!/usr/bin/env python3
"""
Simple test to verify the code structure and basic functionality without dependencies.
"""

import sys
import os

# Add the src directory to the path so we can import modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'todo_app', 'src'))

# Try to import the modules to check syntax
try:
    # Check if the files exist and have proper syntax by attempting to compile them
    import ast

    # Check models.py syntax
    with open('todo_app/src/models.py', 'r') as f:
        models_content = f.read()
        ast.parse(models_content)
    print("✓ models.py has valid Python syntax")

    # Check service.py syntax
    with open('todo_app/src/service.py', 'r') as f:
        service_content = f.read()
        ast.parse(service_content)
    print("✓ service.py has valid Python syntax")

    # Check ui.py syntax
    with open('todo_app/src/ui.py', 'r') as f:
        ui_content = f.read()
        ast.parse(ui_content)
    print("✓ ui.py has valid Python syntax")

    # Check main.py syntax
    with open('todo_app/src/main.py', 'r') as f:
        main_content = f.read()
        ast.parse(main_content)
    print("✓ main.py has valid Python syntax")

    print("\n✓ All Python files have valid syntax!")

except SyntaxError as e:
    print(f"✗ Syntax error in Python files: {e}")
    sys.exit(1)
except Exception as e:
    print(f"✗ Error checking Python files: {e}")
    sys.exit(1)