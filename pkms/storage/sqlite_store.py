from __future__ import annotations

import sqlite3
from pathlib import Path
from typing import List
from datetime import datetime

from pkms.models import Task


SCHEMA = """
CREATE TABLE IF NOT EXISTS tasks (
  id INTEGER PRIMARY KEY AUTOINCREMENT,
  title TEXT NOT NULL,
  priority TEXT NOT NULL,
  due TEXT,
  tags TEXT,
  note TEXT,
  created_at TEXT NOT NULL,
  done INTEGER NOT NULL DEFAULT 0,
  done_at TEXT
);
"""


class SQLiteStore:
    def __init__(self, path: Path | str) -> None:
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with sqlite3.connect(self.path) as con:
            con.execute(SCHEMA)

    def _row_to_task(self, row) -> Task:
        (id_, title, priority, due, tags, note, created_at, done, done_at) = row
        return Task.from_dict(
            {
                "id": id_,
                "title": title,
                "priority": priority,
                "due": due,
                "tags": (tags.split(",") if tags else []),
                "note": note,
                "created_at": created_at,
                "done": bool(done),
                "done_at": done_at,
            }
        )

    def list(self, include_done: bool = False) -> List[Task]:
        with sqlite3.connect(self.path) as con:
            cur = con.execute(
                "SELECT id, title, priority, due, tags, note, created_at, done, done_at FROM tasks"
                + ("" if include_done else " WHERE done = 0")
                + " ORDER BY id"
            )
            return [self._row_to_task(r) for r in cur.fetchall()]

    def add(self, t: Task) -> int:
        with sqlite3.connect(self.path) as con:
            cur = con.execute(
                "INSERT INTO tasks (title, priority, due, tags, note, created_at, done, done_at)"
                " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
                (
                    t.title,
                    t.priority,
                    (t.due.isoformat() if t.due else None),
                    ("".join([]) if not t.tags else ",".join(t.tags)),
                    t.note,
                    t.created_at.isoformat(),
                    int(t.done),
                    (t.done_at.isoformat() if t.done_at else None),
                ),
            )
            return int(cur.lastrowid)

    def complete(self, task_id: int) -> bool:
        with sqlite3.connect(self.path) as con:
            cur = con.execute(
                "UPDATE tasks SET done = 1, done_at = ? WHERE id = ? AND done = 0",
                (datetime.utcnow().isoformat(), task_id),
            )
            return cur.rowcount > 0

    def delete(self, task_id: int) -> bool:
        with sqlite3.connect(self.path) as con:
            cur = con.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
            return cur.rowcount > 0

    def search(self, keyword: str) -> List[Task]:
        kw = f"%{keyword.lower()}%"
        with sqlite3.connect(self.path) as con:
            cur = con.execute(
                "SELECT id, title, priority, due, tags, note, created_at, done, done_at"
                " FROM tasks WHERE lower(title) LIKE ? OR lower(note) LIKE ?",
                (kw, kw),
            )
            return [self._row_to_task(r) for r in cur.fetchall()]
