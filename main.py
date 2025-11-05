from __future__ import annotations
import argparse
import os
from datetime import date, datetime, timedelta
from pathlib import Path
from typing import List, Optional

# Storage backends (keep these module names matching your repo)
from pkms.storage.json_store import JSONStore
from pkms.storage.sqlite_store import SQLiteStore
# Your Task model should live in pkms/models.py; adapt imports if different.
from pkms.models import Task  # expects dataclass with fields similar to: id,title,priority,due,tags,note,created_at,done,done_at

# --- Optional LLM adapter (non-fatal if missing) ----------------------------
try:
    # Expect a function like: respond(prompt: str, system: str | None = None) -> str
    from pkms.llm_adapter import respond as llm_respond  # type: ignore
except Exception:  # module not present or not configured
    llm_respond = None  # noqa: F401

# --- Defaults / constants ---------------------------------------------------
DEFAULT_DB = Path("~/.pkms/tasks.db").expanduser()
DEFAULT_JSON = Path("~/.pkms/tasks.json").expanduser()
PRIORITIES = ("low", "normal", "high", "urgent")


# --- Helpers ----------------------------------------------------------------
def parse_date(s: Optional[str]) -> Optional[date]:
    if not s:
        return None
    return date.fromisoformat(s)


def fmt_task(t: Task) -> str:
    due = t.due.isoformat() if t.due else "—"
    tags = ",".join(t.tags) if getattr(t, "tags", None) else "—"
    status = "✓" if t.done else " "
    return f"[{status}] #{t.id} | {t.title} | p:{t.priority} | due:{due} | tags:{tags}"


def get_store(args):
    if args.storage == "sqlite":
        return SQLiteStore(args.db_path or DEFAULT_DB)
    return JSONStore(args.json_path or DEFAULT_JSON)


# --- AI agent (heuristic + optional LLM) ------------------------------------
class AIAgent:
    """Rank and suggest using a simple heuristic; optionally enrich with LLM if available."""
    _p_rank = {"urgent": 0, "high": 1, "normal": 2, "low": 3}

    def prioritize(self, tasks: List[Task]) -> List[Task]:
        def score(t: Task):
            return (
                self._p_rank.get(t.priority, 2),
                t.due or date.max,
                t.id or 0,
            )
        return sorted(tasks, key=score)

    def suggest_next_action(self, tasks: List[Task]) -> str:
        if not tasks:
            return "No tasks pending. Add one high-impact task for this week."

        ranked = self.prioritize(tasks)
        top = ranked[:3]

        # Heuristic suggestion
        suggestion = [
            "Focus for the next 90 minutes:",
            f"1) Deep work on #{top[0].id}: {top[0].title} (set a 25-min timer)."
        ]
        if len(top) > 1:
            others = ", ".join(f"#{t.id}" for t in top[1:])
            suggestion.append(f"2) Quick wins on {others}.")
        suggestion.append("Capture blockers in notes.")

        base_text = "\n".join(suggestion)

        # Optionally enrich with LLM if available and env allows it
        if llm_respond and os.getenv("PKMS_ENABLE_LLM", "0") in {"1", "true", "True"}:
            try:
                tasks_bullets = "\n".join(f"- {fmt_task(t)}" for t in ranked[:10])
                prompt = (
                    "Based on these tasks, give a 3-step, concise, actionable plan:\n"
                    f"{tasks_bullets}\n"
                    "Keep it under 80 words. Prefer specific verbs and timeboxes."
                )
                llm = llm_respond(prompt, system="You are a concise productivity coach.")
                if llm and isinstance(llm, str):
                    return f"{base_text}\n\nAI coach:\n{llm.strip()}"
            except Exception:
                pass  # silently fall back to heuristic

        return base_text

    def weekly_summary(self, completed: List[Task], upcoming: List[Task]) -> str:
        return (
            f"Completed last 7 days: {len(completed)} | Upcoming (7d): {len(upcoming)}\n"
            "Tip: batch similar tasks and timebox into 25-minute sprints."
        )


# --- Commands ---------------------------------------------------------------
def cmd_add(args):
    store = get_store(args)
    t = Task(
        id=None,
        title=args.title,
        priority=args.priority,
        due=parse_date(args.due),
        tags=args.tag or [],
        note=args.note,
        created_at=datetime.utcnow(),
        done=False,
        done_at=None,
    )
    new_id = store.add(t)
    print(f"✅ Added task #{new_id}: {t.title}")


def cmd_list(args):
    store = get_store(args)
    tasks = store.list(include_done=args.all)
    if not tasks:
        print("(no tasks)")
        return
    for t in tasks:
        print(fmt_task(t))
        if getattr(t, "note", None):
            print(f"    note: {t.note}")


def cmd_done(args):
    store = get_store(args)
    ok = store.complete(args.id)
    print("✅ Marked done" if ok else "(no change)")


def cmd_delete(args):
    store = get_store(args)
    ok = store.delete(args.id)
    print("🗑️  Deleted" if ok else "(not found)")


def cmd_search(args):
    store = get_store(args)
    hits = store.search(args.keyword)
    if not hits:
        print("(no matches)")
        return
    for t in hits:
        print(fmt_task(t))


def cmd_prioritize(args):
    store = get_store(args)
    tasks = store.list(include_done=False)
    agent = AIAgent()
    ranked = agent.prioritize(tasks)
    if not ranked:
        print("(no tasks)")
        return
    for t in ranked:
        print(fmt_task(t))


def cmd_suggest(args):
    store = get_store(args)
    tasks = store.list(include_done=False)
    agent = AIAgent()
    print(agent.suggest_next_action(tasks))


def cmd_weekly_summary(args):
    store = get_store(args)
    today = date.today()
    all_tasks = store.list(include_done=True)
    completed = [
        t for t in all_tasks
        if t.done and getattr(t, "done_at", None) and (today - t.done_at.date()).days <= 7
    ]
    upcoming = [
        t for t in store.list(include_done=False)
        if t.due and 0 <= (t.due - today).days <= 7
    ]
    agent = AIAgent()
    print(agent.weekly_summary(completed, upcoming))


# --- Main -------------------------------------------------------------------
def main(argv: list[str] | None = None):
    # If run without arguments, launch web interface
    if argv is None:
        import sys
        if len(sys.argv) == 1:
            print("No command provided. Launching web interface...")
            print("(Use --help to see CLI commands)")
            import subprocess
            subprocess.run([sys.executable, "web_app.py"])
            return 0
    
    p = argparse.ArgumentParser(prog="pkms", description="AI-powered Task Manager (PKMS)")
    p.add_argument("--storage", choices=["sqlite", "json"], default="sqlite")
    p.add_argument("--db-path", default=None, help="path to SQLite DB (for --storage sqlite)")
    p.add_argument("--json-path", default=None, help="path to JSON file (for --storage json)")

    sub = p.add_subparsers(dest="cmd", required=False)

    sp = sub.add_parser("add", help="add a new task")
    sp.add_argument("title")
    sp.add_argument("--priority", choices=list(PRIORITIES), default="normal")
    sp.add_argument("--due", help="YYYY-MM-DD")
    sp.add_argument("--tag", action="append", help="repeat for multiple tags")
    sp.add_argument("--note")
    sp.set_defaults(func=cmd_add)

    sp = sub.add_parser("list", help="list tasks")
    sp.add_argument("--all", action="store_true", help="include completed tasks")
    sp.set_defaults(func=cmd_list)

    sp = sub.add_parser("done", help="mark a task complete")
    sp.add_argument("id", type=int)
    sp.set_defaults(func=cmd_done)

    sp = sub.add_parser("delete", help="delete a task")
    sp.add_argument("id", type=int)
    sp.set_defaults(func=cmd_delete)

    sp = sub.add_parser("search", help="search tasks by keyword")
    sp.add_argument("keyword")
    sp.set_defaults(func=cmd_search)

    sp = sub.add_parser("prioritize", help="rank tasks by urgency/impact")
    sp.set_defaults(func=cmd_prioritize)

    sp = sub.add_parser("suggest", help="AI next-best-action suggestion")
    sp.set_defaults(func=cmd_suggest)

    sp = sub.add_parser("weekly-summary", help="summary of completed and upcoming")
    sp.set_defaults(func=cmd_weekly_summary)

    args = p.parse_args(argv)
    if hasattr(args, 'func'):
        args.func(args)
    else:
        # No command provided, show help
        p.print_help()


if __name__ == "__main__":
    raise SystemExit(main())
