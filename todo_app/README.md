# Phase I In-Memory Python Console Todo Application

A command-line todo management application built with Python 3.13+ and Pydantic for data validation. Part of a progressive complexity series transitioning from console to cloud-native applications.

## Features

- **Full CRUD Operations**: Create, Read, Update, Delete, and Mark Complete todos
- **Menu-Driven Interface**: Easy-to-use numbered menu system
- **Data Validation**: Title length, required fields, and enum validation
- **Error Handling**: User-friendly error messages with guidance
- **Session-Based Storage**: In-memory storage for single-session use

## Requirements

- Python 3.13+
- Pydantic 2.x
- pytest (for testing)

## Installation

1. Clone or download the repository
2. Navigate to the `todo_app` directory
3. Install dependencies using uv (recommended):
   ```bash
   uv sync
   ```
   Or install using pip:
   ```bash
   pip install pydantic pytest
   ```

## Usage

Run the application using:
```bash
python -m src.main
```

Or with uv:
```bash
uv run python -m src.main
```

### Menu Options

1. **Add Todo**: Create a new todo with title, description, and priority
2. **View Todos**: Display all todos in a table format
3. **Update Todo**: Modify existing todo attributes
4. **Delete Todo**: Remove a todo by ID
5. **Mark Complete**: Change a todo's status to completed
6. **Exit**: Quit the application

### Example Workflow

1. Launch the application
2. Select "Add Todo" to create a new task
3. Select "View Todos" to see your tasks
4. Use "Update Todo" or "Mark Complete" to manage tasks
5. Use "Delete Todo" to remove completed tasks
6. Exit when finished

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
│   ├── test_service.py  # Unit tests for CRUD operations
│   ├── test_integration.py  # Integration tests
│   └── test_ui.py       # UI component tests
├── pyproject.toml       # UV configuration with dependencies
├── README.md            # Setup and usage instructions
└── .gitignore           # Python-specific gitignore
```

## Development

### Running Tests

Execute all tests with:
```bash
pytest
```

Or with uv:
```bash
uv run pytest
```

To run tests with coverage:
```bash
pytest --cov=src --cov-report=html
```

### Architecture

The application follows clean architecture principles:

- **Models** (`models.py`): Pydantic models for data validation
- **Service** (`service.py`): Business logic and data operations
- **UI** (`ui.py`): Console interface and user interaction
- **Main** (`main.py`): Application entry point and orchestration

## Testing

The application includes comprehensive tests:

- Unit tests for all service layer methods
- Integration tests for end-to-end functionality
- Validation tests for error conditions
- Edge case tests for non-existent IDs and empty lists

Achieves >59% code coverage (excluding main.py entry point).

## Phase I Constraints

- **In-Memory Storage**: Data is lost when the application exits
- **Single Session**: Data persists only during current session
- **Console-Only Interface**: No GUI or web interface
- **Single User**: Designed for single-user sessions

## Future Phases

- Phase II: Add database persistence and web interface
- Phase III: Integrate AI-powered natural language processing
- Phase IV: Deploy with containerization and orchestration
- Phase V: Scale to cloud-native architecture

## Contributing

This application is part of an educational series on progressive complexity and spec-driven development. Contributions are welcome, especially around:

- Bug fixes
- Performance improvements
- Test coverage enhancements
- Documentation improvements

## License

This project is part of the Phase-Based Todo Application series demonstrating spec-driven development methodologies.