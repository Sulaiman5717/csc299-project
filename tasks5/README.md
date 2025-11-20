# Tasks Manager (Spec-Kit)

A simple command-line task management application built using GitHub's spec-kit framework for spec-driven development.

## Overview

This project was created using the spec-kit toolkit, which enables spec-driven development. The tasks manager provides basic task management functionality through a clean CLI interface.

## Features

- Create and manage tasks
- Mark tasks as complete/incomplete  
- List all tasks
- Delete tasks
- Persistent storage using JSON

## Installation

```bash
# Install dependencies
uv sync

# Or install in editable mode
uv pip install -e .
```

## Usage

The package requires PYTHONPATH to be set to the src directory:

```bash
# Add a task
PYTHONPATH=src uv run python -m tasks_manager add "Buy groceries"

# List all tasks  
PYTHONPATH=src uv run python -m tasks_manager list

# Complete a task (toggle completion status)
PYTHONPATH=src uv run python -m tasks_manager complete 1

# Delete a task
PYTHONPATH=src uv run python -m tasks_manager delete 1

# Show help
PYTHONPATH=src uv run python -m tasks_manager help
```

## Project Structure

```
tasks5/
├── .github/           # Spec-kit agent definitions and prompts
├── .specify/          # Spec-kit configuration and templates
├── src/
│   └── tasks_manager/ # Main application code
│       ├── __init__.py
│       ├── __main__.py  # CLI entry point
│       ├── task.py      # Task data model
│       └── store.py     # JSON storage manager
├── pyproject.toml     # Project configuration
└── README.md
```

## Spec-Kit Integration

This project was initialized with spec-kit using:

```bash
specify init tasks-manager --ai copilot
```

The `.github/` directory contains agent definitions for spec-driven development workflows:
- `/speckit.constitution` - Project principles
- `/speckit.specify` - Create specifications  
- `/speckit.plan` - Implementation planning
- `/speckit.tasks` - Task generation
- `/speckit.implement` - Code implementation

## Data Storage

Tasks are stored in a `tasks.json` file in the current working directory. The file is automatically created on first use.

## Development

This project follows spec-driven development principles using GitHub's spec-kit framework, which emphasizes:

1. Clear specifications before implementation
2. AI-assisted development workflows
3. Structured project organization
4. Predictable development outcomes
