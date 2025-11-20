"""Command-line interface for tasks manager."""

import sys
from .store import TaskStore


def print_task(task):
    """Print a single task."""
    status = "✓" if task.completed else " "
    print(f"[{status}] {task.id}. {task.title}")


def cmd_add(store: TaskStore, args: list):
    """Add a new task."""
    if not args:
        print("Error: Please provide a task title")
        sys.exit(1)
    
    title = " ".join(args)
    task = store.add_task(title)
    print(f"Added task: {task.title} (ID: {task.id})")


def cmd_list(store: TaskStore, args: list):
    """List all tasks."""
    tasks = store.get_all_tasks()
    
    if not tasks:
        print("No tasks found.")
        return
    
    print(f"\nYou have {len(tasks)} task(s):\n")
    for task in tasks:
        print_task(task)
    print()


def cmd_complete(store: TaskStore, args: list):
    """Mark a task as complete."""
    if not args:
        print("Error: Please provide a task ID")
        sys.exit(1)
    
    try:
        task_id = int(args[0])
    except ValueError:
        print(f"Error: Invalid task ID: {args[0]}")
        sys.exit(1)
    
    task = store.toggle_complete(task_id)
    if task:
        status = "completed" if task.completed else "uncompleted"
        print(f"Task {task_id} marked as {status}")
    else:
        print(f"Error: Task {task_id} not found")
        sys.exit(1)


def cmd_delete(store: TaskStore, args: list):
    """Delete a task."""
    if not args:
        print("Error: Please provide a task ID")
        sys.exit(1)
    
    try:
        task_id = int(args[0])
    except ValueError:
        print(f"Error: Invalid task ID: {args[0]}")
        sys.exit(1)
    
    if store.delete_task(task_id):
        print(f"Deleted task {task_id}")
    else:
        print(f"Error: Task {task_id} not found")
        sys.exit(1)


def show_help():
    """Show help message."""
    print("""
Tasks Manager - Simple command-line task management

Usage: uv run python -m tasks_manager <command> [arguments]

Commands:
  add <title>       Add a new task
  list              List all tasks
  complete <id>     Toggle task completion status
  delete <id>       Delete a task
  help              Show this help message

Examples:
  uv run python -m tasks_manager add "Buy groceries"
  uv run python -m tasks_manager list
  uv run python -m tasks_manager complete 1
  uv run python -m tasks_manager delete 1
""")


def main():
    """Main entry point for CLI."""
    if len(sys.argv) < 2:
        show_help()
        sys.exit(1)
    
    command = sys.argv[1]
    args = sys.argv[2:]
    
    if command == "help":
        show_help()
        return
    
    store = TaskStore()
    
    commands = {
        "add": cmd_add,
        "list": cmd_list,
        "complete": cmd_complete,
        "delete": cmd_delete,
    }
    
    if command not in commands:
        print(f"Error: Unknown command '{command}'")
        show_help()
        sys.exit(1)
    
    commands[command](store, args)


if __name__ == "__main__":
    main()
