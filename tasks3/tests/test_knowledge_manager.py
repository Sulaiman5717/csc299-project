from pathlib import Path
from tasks3.knowledge_manager import KnowledgeManager


def test_add_and_search_entry(tmp_path: Path):
    km = KnowledgeManager(data_dir=str(tmp_path))
    e1 = km.add_entry(
        title="pytest tips",
        content="Use tmp_path fixture",
        categories=["testing"],
        tags=["pytest", "tips"],
    )
    e2 = km.add_entry(
        title="docs",
        content="Write clear docs",
        categories=["docs"],
        tags=["writing"],
    )

    results = km.search_entries(query="write")
    assert {e.title for e in results} == {"docs"}

    by_cat = km.get_entries_by_category()
    assert "testing" in by_cat and any(x.id == e1.id for x in by_cat["testing"])

    assert km.link_to_task(e1.id, 42) is True
    assert 42 in km.get_entry(e1.id).related_tasks
