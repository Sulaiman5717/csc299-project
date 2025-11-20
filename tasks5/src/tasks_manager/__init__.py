"""Tasks Manager - A simple command-line task management application."""

from .task import Task
from .store import TaskStore

__version__ = "0.1.0"
__all__ = ["Task", "TaskStore"]
