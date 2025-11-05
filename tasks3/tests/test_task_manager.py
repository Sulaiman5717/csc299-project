from pathlib import Path
from tasks3.task_manager import TaskManager


def test_add_and_get_task(tmp_path: Path):
    tm = TaskManager(data_dir=str(tmp_path))
    t = tm.add_task("Write tests", "Add pytest tests", priority="high", tags=["dev"])

    fetched = tm.get_task(t.id)
    assert fetched is not None
    assert fetched.title == "Write tests"
    assert fetched.priority == "high"
    assert "dev" in fetched.tags


def test_search_and_update(tmp_path: Path):
    tm = TaskManager(data_dir=str(tmp_path))
    t1 = tm.add_task("Doc", "Write docs", priority="normal", categories=["docs"]) 
    t2 = tm.add_task("Test", "Write tests", priority="high", categories=["qa"], tags=["pytest"]) 

    # search by query
    results = tm.search_tasks(query="write")
    assert {t.title for t in results} == {"Doc", "Test"}

    # update and group by status/priority
    tm.update_task(t1.id, status="completed")
    by_status = tm.get_tasks_by_status()
    assert len(by_status["completed"]) == 1
    assert by_status["completed"][0].id == t1.id

    by_priority = tm.get_tasks_by_priority()
    assert any(task.id == t2.id for task in by_priority["high"])
