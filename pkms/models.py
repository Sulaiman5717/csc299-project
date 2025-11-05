from __future__ import annotations

from dataclasses import dataclass
from datetime import date, datetime
from typing import Optional, List, Dict, Any


@dataclass
class Task:
    id: Optional[int]
    title: str
    priority: str
    due: Optional[date]
    tags: List[str]
    note: Optional[str]
    created_at: datetime
    done: bool
    done_at: Optional[datetime]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "title": self.title,
            "priority": self.priority,
            "due": self.due.isoformat() if self.due else None,
            "tags": list(self.tags) if self.tags else [],
            "note": self.note,
            "created_at": self.created_at.isoformat(),
            "done": self.done,
            "done_at": self.done_at.isoformat() if self.done_at else None,
        }

    @staticmethod
    def from_dict(data: Dict[str, Any]) -> "Task":
        d = data.copy()
        # parse dates/datetimes
        due = d.get("due")
        if isinstance(due, str):
            d["due"] = date.fromisoformat(due)
        created_at = d.get("created_at")
        if isinstance(created_at, str):
            d["created_at"] = datetime.fromisoformat(created_at)
        done_at = d.get("done_at")
        if isinstance(done_at, str):
            d["done_at"] = datetime.fromisoformat(done_at)
        # normalize lists
        tags = d.get("tags")
        if tags is None:
            d["tags"] = []
        return Task(**d)
