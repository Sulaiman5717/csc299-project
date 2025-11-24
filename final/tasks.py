import json
import sys
import os

DATA_FILE = "tasks_data.json"

def load_tasks():
    if not os.path.exists(DATA_FILE):
        return []
    with open(DATA_FILE, "r") as f:
        return json.load(f)

def save_tasks(tasks):
    with open(DATA_FILE, "w") as f:
        json.dump(tasks, f, indent=4)

def add_task(description):
    tasks = load_tasks()
    task = {"id": len(tasks) + 1, "description": description}
    tasks.append(task)
    save_tasks(tasks)
    print(f"✅ Added task: {description}")

def list_tasks():
    tasks = load_tasks()
    if not tasks:
        print("No tasks found.")
    else:
        print("📋 Task List:")
        for task in tasks:
            print(f"{task['id']}: {task['description']}")

def search_tasks(keyword):
    tasks = load_tasks()
    matches = [t for t in tasks if keyword.lower() in t["description"].lower()]
    if matches:
        print("🔍 Search results:")
        for t in matches:
            print(f"{t['id']}: {t['description']}")
    else:
        print("No matching tasks found.")

def main():
    if len(sys.argv) < 2:
        print("Usage: python tasks.py [add|list|search] [arguments]")
        return

    command = sys.argv[1]

    if command == "add" and len(sys.argv) > 2:
        description = " ".join(sys.argv[2:])
        add_task(description)
    elif command == "list":
        list_tasks()
    elif command == "search" and len(sys.argv) > 2:
        keyword = " ".join(sys.argv[2:])
        search_tasks(keyword)
    else:
        print("Invalid command or missing arguments.")

if __name__ == "__main__":
    main()
