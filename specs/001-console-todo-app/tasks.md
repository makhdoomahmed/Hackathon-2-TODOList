# Tasks: Phase I In-Memory Python Console Todo Application

**Feature**: Phase I In-Memory Python Console Todo Application
**Target**: MVP with full CRUD functionality and menu-driven interface
**Strategy**: Implement in priority order of user stories, with foundational components first

## Dependencies Between User Stories

**User Story Order**: US1 (P1) → US4 (P1) → US2 (P2) → US3 (P3)
- US1 (Create/View) is foundational for all others
- US4 (Navigation) needed by all stories for user interaction
- US2 (Update Status) builds on US1 functionality
- US3 (Modify/Delete) builds on US1 functionality

## Parallel Execution Examples

**Per Story Parallelism**:
- US1: Model definition [P] can run in parallel with service skeleton [P]
- US4: Menu UI [P] can run in parallel with input validation [P]
- US2: Mark complete function [P] can run in parallel with update function [P]
- US3: Update function [P] can run in parallel with delete function [P]

## Implementation Strategy

**MVP First**: Implement US1 (Create/View) completely before moving to other stories. This delivers the core value proposition (basic todo tracking) early. Each subsequent user story adds incremental value without breaking existing functionality.

---

## Phase 1: Setup and Project Initialization

- [ ] T001 Create project directory structure: todo_app/src/, todo_app/tests/, todo_app/pyproject.toml, todo_app/README.md, todo_app/.gitignore
- [ ] T002 Initialize pyproject.toml with Python 3.13+, Pydantic, and pytest dependencies
- [ ] T003 Create empty __init__.py files in src/ and tests/ directories
- [ ] T004 Set up .gitignore with Python-specific exclusions

## Phase 2: Foundational Components

- [ ] T005 Define TodoStatus and TodoPriority enums in preparation for model
- [ ] T006 Create Todo Pydantic model in src/models.py with all required fields and validation
- [ ] T007 Implement TodoService class skeleton in src/service.py with in-memory storage and ID counter
- [ ] T008 Create basic UI structure in src/ui.py with placeholder methods
- [ ] T009 Create main.py entry point with basic structure

## Phase 3: User Story 1 - Create and View Todos (Priority: P1)

**Goal**: Enable users to create new todo items and view them in a list to track tasks they need to complete. This is the core functionality that delivers immediate value.

**Independent Test**: Can be fully tested by launching the application, adding 2-3 todos with different priorities, and viewing the list. Delivers immediate value as a basic task tracker.

- [ ] T010 [P] [US1] Implement add_todo method in TodoService with validation for title length and emptiness
- [ ] T011 [P] [US1] Implement get_all_todos method in TodoService to return all todos sorted by ID
- [ ] T012 [US1] Implement create todo functionality in UI layer with input prompts and validation
- [ ] T013 [US1] Implement view todos functionality in UI layer with table-like display format
- [ ] T014 [US1] Integrate create todo UI with service layer
- [ ] T015 [US1] Integrate view todos UI with service layer
- [ ] T016 [US1] Add error handling for empty title validation in create todo flow
- [ ] T017 [US1] Add error handling for title length validation (max 100 chars)
- [ ] T018 [US1] Test basic create and view functionality end-to-end

## Phase 4: User Story 4 - Navigate Application Interface (Priority: P1)

**Goal**: Provide a clear menu system with input validation so users can use the application without confusion or errors. Critical for usability since even basic CRUD operations are useless if users can't navigate the interface.

**Independent Test**: Launch the application and navigate through all menu options, including entering invalid inputs, to verify the interface is intuitive and error-handling works correctly.

- [ ] T019 [P] [US4] Implement main menu display in UI layer with numbered options for all 6 operations
- [ ] T020 [P] [US4] Implement menu navigation loop in main.py that stays active until exit
- [ ] T021 [US4] Implement input validation for menu selection with error message for invalid options
- [ ] T022 [US4] Implement return to main menu after each operation completes (success or failure)
- [ ] T023 [US4] Implement exit functionality with goodbye message
- [ ] T024 [US4] Test menu navigation with valid and invalid inputs
- [ ] T025 [US4] Test that application returns to menu after each operation

## Phase 5: User Story 2 - Update Todo Status (Priority: P2)

**Goal**: Enable users to mark todos as in-progress or completed to track their progress on tasks. Builds on US1 functionality.

**Independent Test**: Create a todo using P1 functionality, then mark it as "in_progress", then mark it as "completed". View the list to verify status changes persisted.

- [ ] T026 [P] [US2] Implement mark_complete method in TodoService to change status to "completed"
- [ ] T027 [P] [US2] Implement get_todo_by_id method in TodoService for retrieving specific todos
- [ ] T028 [US2] Implement mark complete functionality in UI layer with ID input and validation
- [ ] T029 [US2] Implement update_todo method in TodoService for partial updates (status field)
- [ ] T030 [US2] Implement update todo functionality in UI layer for status changes
- [ ] T031 [US2] Integrate mark complete UI with service layer
- [ ] T032 [US2] Integrate update status UI with service layer
- [ ] T033 [US2] Add error handling for non-existent ID in mark complete flow
- [ ] T034 [US2] Add error handling for non-existent ID in update status flow
- [ ] T035 [US2] Test mark complete functionality end-to-end
- [ ] T036 [US2] Test update status functionality end-to-end

## Phase 6: User Story 3 - Modify and Delete Todos (Priority: P3)

**Goal**: Allow users to edit todo details and remove completed or cancelled tasks to keep their list accurate and relevant. Completes the full CRUD functionality.

**Independent Test**: Create a todo, update its title and description, then delete it. Verify the todo list reflects all changes correctly.

- [ ] T037 [P] [US3] Implement delete_todo method in TodoService with proper ID handling
- [ ] T038 [P] [US3] Implement update_todo method in TodoService for all fields (title, description, priority)
- [ ] T039 [US3] Implement delete todo functionality in UI layer with ID input and validation
- [ ] T040 [US3] Implement full update todo functionality in UI layer for all attributes
- [ ] T041 [US3] Integrate delete UI with service layer
- [ ] T042 [US3] Integrate full update UI with service layer
- [ ] T043 [US3] Add error handling for non-existent ID in delete flow
- [ ] T044 [US3] Add error handling for non-existent ID in update flow
- [ ] T045 [US3] Add validation for title length and emptiness in update flow
- [ ] T046 [US3] Test delete functionality end-to-end
- [ ] T047 [US3] Test full update functionality end-to-end

## Phase 7: Error Handling and Edge Cases

- [ ] T048 Implement handling for empty todo list in view functionality
- [ ] T049 Implement validation for invalid priority values in input
- [ ] T050 Implement validation for invalid status values in input
- [ ] T051 Implement handling for empty title in update flow
- [ ] T052 Implement handling for title length in update flow
- [ ] T053 Add comprehensive error messages with guidance for all validation failures
- [ ] T054 Test all edge cases identified in specification

## Phase 8: Testing and Quality Assurance

- [ ] T055 [P] Create test_service.py in tests/ directory
- [ ] T056 [P] Write unit tests for all TodoService CRUD operations
- [ ] T057 Write tests for data validation (title length, priority values, etc.)
- [ ] T058 Write tests for edge cases (empty list, non-existent IDs, etc.)
- [ ] T059 Run pytest to verify test coverage is ≥80%
- [ ] T060 Fix any failing tests and ensure all requirements are met

## Phase 9: Polish and Documentation

- [ ] T061 Add type hints to all functions and methods as required by constitution
- [ ] T062 Add Google-style docstrings to all public functions
- [ ] T063 Update README.md with installation and usage instructions
- [ ] T064 Test full application workflow: create → view → update → delete → exit
- [ ] T065 Verify all functional requirements from spec are met
- [ ] T066 Run application and verify all 5 CRUD operations work correctly