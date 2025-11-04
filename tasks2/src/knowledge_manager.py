from __future__ import annotations
from dataclasses import dataclass, asdict
from datetime import datetime
from pathlib import Path
from typing import List, Optional, Dict
import json

@dataclass
class KnowledgeEntry:
    """Enhanced knowledge entry model."""
    id: int
    title: str
    content: str
    categories: List[str]
    tags: List[str]
    references: List[str]
    created_at: str
    updated_at: str
    related_tasks: List[int]  # IDs of related tasks
    
    @staticmethod
    def from_dict(data: Dict) -> KnowledgeEntry:
        return KnowledgeEntry(**data)
    
    def to_dict(self) -> Dict:
        return asdict(self)

class KnowledgeManager:
    """Enhanced knowledge management system."""
    
    def __init__(self, data_dir: str = "data"):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(parents=True, exist_ok=True)
        self.knowledge_file = self.data_dir / "knowledge.json"
        self.entries: List[KnowledgeEntry] = []
        self.load_entries()

    def load_entries(self):
        """Load knowledge entries from JSON file."""
        if not self.knowledge_file.exists():
            self.entries = []
            return
            
        try:
            with open(self.knowledge_file, 'r', encoding='utf-8') as f:
                data = json.load(f)
                self.entries = [KnowledgeEntry.from_dict(entry_data) for entry_data in data]
        except Exception as e:
            print(f"Error loading knowledge entries: {e}")
            self.entries = []

    def save_entries(self):
        """Save knowledge entries to JSON file."""
        try:
            with open(self.knowledge_file, 'w', encoding='utf-8') as f:
                data = [entry.to_dict() for entry in self.entries]
                json.dump(data, f, indent=2)
        except Exception as e:
            print(f"Error saving knowledge entries: {e}")

    def add_entry(self, title: str, content: str, categories: List[str] = None,
                tags: List[str] = None, references: List[str] = None,
                related_tasks: List[int] = None) -> KnowledgeEntry:
        """Add a new knowledge entry with enhanced metadata."""
        entry_id = len(self.entries) + 1
        now = datetime.now().isoformat()
        
        entry = KnowledgeEntry(
            id=entry_id,
            title=title,
            content=content,
            categories=categories or [],
            tags=tags or [],
            references=references or [],
            created_at=now,
            updated_at=now,
            related_tasks=related_tasks or []
        )
        
        self.entries.append(entry)
        self.save_entries()
        return entry

    def get_entry(self, entry_id: int) -> Optional[KnowledgeEntry]:
        """Get a knowledge entry by ID."""
        return next((entry for entry in self.entries if entry.id == entry_id), None)

    def update_entry(self, entry_id: int, **kwargs) -> Optional[KnowledgeEntry]:
        """Update knowledge entry attributes."""
        entry = self.get_entry(entry_id)
        if not entry:
            return None
            
        for key, value in kwargs.items():
            if hasattr(entry, key):
                setattr(entry, key, value)
                
        entry.updated_at = datetime.now().isoformat()
        self.save_entries()
        return entry

    def delete_entry(self, entry_id: int) -> bool:
        """Delete a knowledge entry."""
        entry = self.get_entry(entry_id)
        if entry:
            self.entries.remove(entry)
            self.save_entries()
            return True
        return False

    def search_entries(self, query: str = None, categories: List[str] = None,
                     tags: List[str] = None, related_task_id: int = None) -> List[KnowledgeEntry]:
        """Enhanced search with multiple criteria."""
        results = self.entries

        if query:
            query = query.lower()
            results = [
                entry for entry in results
                if query in entry.title.lower() or
                query in entry.content.lower()
            ]

        if categories:
            results = [
                entry for entry in results
                if any(cat in entry.categories for cat in categories)
            ]

        if tags:
            results = [
                entry for entry in results
                if any(tag in entry.tags for tag in tags)
            ]

        if related_task_id is not None:
            results = [
                entry for entry in results
                if related_task_id in entry.related_tasks
            ]

        return results

    def get_entries_by_category(self) -> Dict[str, List[KnowledgeEntry]]:
        """Group entries by category."""
        categories = {}
        for entry in self.entries:
            for category in entry.categories:
                if category not in categories:
                    categories[category] = []
                categories[category].append(entry)
        return categories

    def link_to_task(self, entry_id: int, task_id: int) -> bool:
        """Link a knowledge entry to a task."""
        entry = self.get_entry(entry_id)
        if entry and task_id not in entry.related_tasks:
            entry.related_tasks.append(task_id)
            self.save_entries()
            return True
        return False