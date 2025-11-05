from __future__ import annotations

import json
from pathlib import Path
from typing import List
from datetime import datetime

from pkms.models import Task


class JSONStore:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        if not self.path.exists():
            self._write([])

    # basic IO helpers
    def _read(self) -> List[Task]:
        data = json.loads(self.path.read_text(encoding="utf-8"))
        return [Task.from_dict(obj) for obj in data]

    def _write(self, tasks: List[Task | dict]) -> None:
        serializable = [t.to_dict() if isinstance(t, Task) else t for t in tasks]
        self.path.write_text(json.dumps(serializable, indent=2), encoding="utf-8")

    # public API used by main.py
    def list(self, include_done: bool = False) -> List[Task]:
        tasks = self._read()
        return tasks if include_done else [t for t in tasks if not t.done]

    def add(self, t: Task) -> int:
        tasks = self._read()
        new_id = (max((x.id or 0) for x in tasks) + 1) if tasks else 1
        t.id = new_id
        tasks.append(t)
        self._write(tasks)
        return new_id

    def complete(self, task_id: int) -> bool:
        tasks = self._read()
        changed = False
        for t in tasks:
            if t.id == task_id and not t.done:
                t.done = True
                t.done_at = datetime.utcnow()
                changed = True
                break
        if changed:
            self._write(tasks)
        return changed

    def delete(self, task_id: int) -> bool:
        tasks = self._read()
        before = len(tasks)
        tasks = [t for t in tasks if t.id != task_id]
        if len(tasks) != before:
            self._write(tasks)
            return True
        return False

    def search(self, keyword: str) -> List[Task]:
        keyword = keyword.lower()
        return [
            t for t in self._read()
            if keyword in t.title.lower() or (t.note and keyword in t.note.lower())
        ]
