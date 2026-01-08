# Quickstart Guide: Phase I In-Memory Python Console Todo Application

## Prerequisites
- Python 3.13+
- UV package manager installed

## Setup
1. Clone or navigate to the project directory
2. Install dependencies: `uv sync` or `pip install -r requirements.txt`
3. Run the application: `python -m src.main` or `uv run python -m src.main`

## Project Structure
```
todo_app/
├── src/
│   ├── __init__.py
│   ├── main.py          # Entry point with menu loop
│   ├── models.py        # Todo data model (Pydantic)
│   ├── service.py       # Business logic (TodoService)
│   └── ui.py            # Console interface (TodoUI)
├── tests/
│   ├── __init__.py
│   └── test_service.py  # Unit tests for CRUD operations
├── pyproject.toml       # UV configuration with dependencies
├── README.md            # Setup and usage instructions
└── .gitignore           # Python-specific gitignore
```

## Running Tests
- Execute: `pytest` or `uv run pytest`
- Target: ≥80% code coverage as required by constitution

## Key Components
- **models.py**: Contains Pydantic Todo model with validation
- **service.py**: TodoService class with CRUD operations and business logic
- **ui.py**: Console interface with menu system and user interaction
- **main.py**: Application entry point with main menu loop

## Development Workflow
1. Implement models first (Pydantic validation)
2. Build service layer (CRUD operations)
3. Create UI layer (menu system)
4. Write tests (≥80% coverage)
5. Integrate and test end-to-end

## Configuration
- No external configuration files (Phase I constraint)
- All settings via code defaults
- Dependencies managed via pyproject.toml