from __future__ import annotations

# Simple utility function for initial pytest check
def inc(n: int) -> int:
    return n + 1


def main() -> None:
    """Entry point for `uv run tasks3`.

    Demonstrates a minimal run of the PKMS: creates managers pointing to a
    local data directory and prints quick summaries. This avoids modifying
    real user data and keeps execution side effects contained.
    """
    from pathlib import Path
    from .task_manager import TaskManager
    from .knowledge_manager import KnowledgeManager

    data_dir = Path(__file__).resolve().parent.parent / "data"
    tm = TaskManager(data_dir=str(data_dir))
    km = KnowledgeManager(data_dir=str(data_dir))

    # Light-touch demo: ensure data dir exists and print quick snapshot
    data_dir.mkdir(parents=True, exist_ok=True)

    print("tasks3 demo")
    print(f"- Data directory: {data_dir}")
    print(f"- Tasks: {len(tm.tasks)} total")
    print(f"- Knowledge entries: {len(km.entries)} total")
