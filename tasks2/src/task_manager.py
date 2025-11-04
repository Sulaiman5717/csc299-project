from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
import json

@dataclass
class Task:
    """Task model with enhanced attributes."""
    id: int
    title: str
    description: str
    priority: str  # low, normal, high, urgent
    due_date: Optional[str]
    status: str  # not-started, in-progress, completed
    categories: List[str]
    tags: List[str]
    created_at: str
    completed_at: Optional[str]
    
    @staticmethod
    def from_dict(data: Dict) -> Task:
        return Task(**data)
    
    def to_dict(self) -> Dict:
        return asdict(self)

class TaskManager:
    """Enhanced task management system with better organization and features."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.tasks_file = self.data_dir / "tasks.json"
        self.tasks: List[Task] = []
        self.load_tasks()

    def load_tasks(self):
        """Load tasks from JSON file."""
        if not self.tasks_file.exists():
            self.tasks = []
            return
            
        try:
            with open(self.tasks_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.tasks = [Task.from_dict(task_data) for task_data in data]
        except Exception as e:
            print(f"Error loading tasks: {e}")
            self.tasks = []

    def save_tasks(self):
        """Save tasks to JSON file."""
        try:
            with open(self.tasks_file, 'w', encoding='utf-8') as f:
                data = [task.to_dict() for task in self.tasks]
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving tasks: {e}")

    def add_task(self, title: str, description: str, priority: str = "normal",
                due_date: Optional[str] = None, categories: List[str] = None,
                tags: List[str] = None) -> Task:
        """Add a new task with enhanced metadata."""
        task_id = len(self.tasks) + 1
        now = datetime.now().isoformat()
        
        task = Task(
            id=task_id,
            title=title,
            description=description,
            priority=priority,
            due_date=due_date,
            status="not-started",
            categories=categories or [],
            tags=tags or [],
            created_at=now,
            completed_at=None
        )
        
        self.tasks.append(task)
        self.save_tasks()
        return task

    def get_task(self, task_id: int) -> Optional[Task]:
        """Get a task by ID."""
        return next((task for task in self.tasks if task.id == task_id), None)

    def update_task(self, task_id: int, **kwargs) -> Optional[Task]:
        """Update task attributes."""
        task = self.get_task(task_id)
        if not task:
            return None
            
        for key, value in kwargs.items():
            if hasattr(task, key):
                setattr(task, key, value)
                
        if 'status' in kwargs and kwargs['status'] == 'completed':
            task.completed_at = datetime.now().isoformat()
            
        self.save_tasks()
        return task

    def delete_task(self, task_id: int) -> bool:
        """Delete a task."""
        task = self.get_task(task_id)
        if task:
            self.tasks.remove(task)
            self.save_tasks()
            return True
        return False

    def search_tasks(self, query: str = None, categories: List[str] = None,
                    tags: List[str] = None, status: str = None,
                    priority: str = None) -> List[Task]:
        """Enhanced search with multiple criteria."""
        results = self.tasks

        if query:
            query = query.lower()
            results = [
                task for task in results
                if query in task.title.lower() or
                query in task.description.lower()
            ]

        if categories:
            results = [
                task for task in results
                if any(cat in task.categories for cat in categories)
            ]

        if tags:
            results = [
                task for task in results
                if any(tag in task.tags for tag in tags)
            ]

        if status:
            results = [task for task in results if task.status == status]

        if priority:
            results = [task for task in results if task.priority == priority]

        return results

    def get_tasks_by_priority(self) -> Dict[str, List[Task]]:
        """Group tasks by priority."""
        priorities = {"urgent": [], "high": [], "normal": [], "low": []}
        for task in self.tasks:
            priorities[task.priority].append(task)
        return priorities

    def get_tasks_by_status(self) -> Dict[str, List[Task]]:
        """Group tasks by status."""
        statuses = {"not-started": [], "in-progress": [], "completed": []}
        for task in self.tasks:
            statuses[task.status].append(task)
        return statuses