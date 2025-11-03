import json
import sys
import os
from datetime import datetime
from pathlib import Path

DATA_FILE = "knowledge_data.json"

def load_knowledge():
    """Load knowledge entries from JSON file."""
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_knowledge(entries):
    """Save knowledge entries to JSON file."""
    with open(DATA_FILE, "w") as f:
        json.dump(entries, f, indent=4)

def add_entry(title, content, tags=None):
    """Add a new knowledge entry."""
    entries = load_knowledge()
    entry = {
        "id": len(entries) + 1,
        "title": title,
        "content": content,
        "tags": tags or [],
        "created_at": datetime.now().isoformat(),
        "updated_at": datetime.now().isoformat()
    }
    entries.append(entry)
    save_knowledge(entries)
    print(f"✅ Added knowledge entry: {title}")

def list_entries():
    """List all knowledge entries."""
    entries = load_knowledge()
    if not entries:
        print("No knowledge entries found.")
    else:
        print("📚 Knowledge Base:")
        for entry in entries:
            tags = ", ".join(entry["tags"]) if entry["tags"] else "no tags"
            print(f"#{entry['id']}: {entry['title']} [{tags}]")
            print(f"   Created: {entry['created_at']}")
            print("   " + "-" * 40)

def search_entries(query):
    """Search knowledge entries by title, content, or tags."""
    entries = load_knowledge()
    query = query.lower()
    matches = [
        e for e in entries
        if query in e["title"].lower() or 
           query in e["content"].lower() or
           any(query in tag.lower() for tag in e["tags"])
    ]
    
    if matches:
        print("🔍 Search results:")
        for entry in matches:
            tags = ", ".join(entry["tags"]) if entry["tags"] else "no tags"
            print(f"#{entry['id']}: {entry['title']} [{tags}]")
    else:
        print("No matching entries found.")

def view_entry(entry_id):
    """View a specific knowledge entry."""
    entries = load_knowledge()
    entry = next((e for e in entries if e["id"] == entry_id), None)
    
    if entry:
        print(f"\n📝 Entry #{entry['id']}: {entry['title']}")
        print("Tags:", ", ".join(entry["tags"]) if entry["tags"] else "no tags")
        print("Created:", entry["created_at"])
        print("-" * 40)
        print(entry["content"])
        print("-" * 40)
    else:
        print("Entry not found.")

def main():
    """Main CLI interface."""
    if len(sys.argv) < 2:
        print("Usage: python knowledge.py [add|list|search|view] [arguments]")
        return

    command = sys.argv[1]

    if command == "add" and len(sys.argv) > 3:
        title = sys.argv[2]
        content = sys.argv[3]
        tags = sys.argv[4].split(",") if len(sys.argv) > 4 else []
        add_entry(title, content, tags)
    elif command == "list":
        list_entries()
    elif command == "search" and len(sys.argv) > 2:
        query = sys.argv[2]
        search_entries(query)
    elif command == "view" and len(sys.argv) > 2:
        try:
            entry_id = int(sys.argv[2])
            view_entry(entry_id)
        except ValueError:
            print("Invalid entry ID")
    else:
        print("Invalid command or missing arguments.")

if __name__ == "__main__":
    main()