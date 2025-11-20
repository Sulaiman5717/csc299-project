"""Task storage manager."""

import json
from pathlib import Path
from typing import List, Optional
from .task import Task


class TaskStore:
    """Manages task persistence using JSON storage."""
    
    def __init__(self, data_file: str = "tasks.json"):
        """Initialize task store.
        
        Args:
            data_file: Path to JSON file for storing tasks
        """
        self.data_file = Path(data_file)
        self._ensure_file_exists()
    
    def _ensure_file_exists(self):
        """Create data file if it doesn't exist."""
        if not self.data_file.exists():
            self.data_file.write_text(json.dumps({"tasks": [], "next_id": 1}))
    
    def _read_data(self) -> dict:
        """Read data from JSON file."""
        try:
            return json.loads(self.data_file.read_text())
        except (json.JSONDecodeError, FileNotFoundError):
            return {"tasks": [], "next_id": 1}
    
    def _write_data(self, data: dict):
        """Write data to JSON file."""
        self.data_file.write_text(json.dumps(data, indent=2))
    
    def add_task(self, title: str) -> Task:
        """Add a new task.
        
        Args:
            title: Task title
            
        Returns:
            The created task
        """
        data = self._read_data()
        task = Task(id=data["next_id"], title=title)
        data["tasks"].append(task.to_dict())
        data["next_id"] += 1
        self._write_data(data)
        return task
    
    def get_all_tasks(self) -> List[Task]:
        """Get all tasks.
        
        Returns:
            List of all tasks
        """
        data = self._read_data()
        return [Task.from_dict(task_data) for task_data in data["tasks"]]
    
    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a specific task by ID.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Task if found, None otherwise
        """
        tasks = self.get_all_tasks()
        for task in tasks:
            if task.id == task_id:
                return task
        return None
    
    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update a task.
        
        Args:
            task_id: ID of the task to update
            **kwargs: Fields to update
            
        Returns:
            Updated task if found, None otherwise
        """
        data = self._read_data()
        for task_data in data["tasks"]:
            if task_data["id"] == task_id:
                task_data.update(kwargs)
                self._write_data(data)
                return Task.from_dict(task_data)
        return None
    
    def delete_task(self, task_id: int) -> bool:
        """Delete a task.
        
        Args:
            task_id: ID of the task to delete
            
        Returns:
            True if task was deleted, False otherwise
        """
        data = self._read_data()
        original_count = len(data["tasks"])
        data["tasks"] = [t for t in data["tasks"] if t["id"] != task_id]
        
        if len(data["tasks"]) < original_count:
            self._write_data(data)
            return True
        return False
    
    def toggle_complete(self, task_id: int) -> Optional[Task]:
        """Toggle task completion status.
        
        Args:
            task_id: ID of the task
            
        Returns:
            Updated task if found, None otherwise
        """
        task = self.get_task(task_id)
        if task:
            return self.update_task(task_id, completed=not task.completed)
        return None
