from __future__ import annotations
import cmd
import shlex
from typing import Optional
from datetime import datetime

from .task_manager import TaskManager
from .knowledge_manager import KnowledgeManager
from .ai_assistant import AIAssistant

class CommandInterface(cmd.Cmd):
    """Enhanced command-line interface with natural language support."""
    
    intro = """
    🚀 Welcome to Personal Knowledge & Task Management System v2
    Type 'help' or '?' to list commands.
    """
    prompt = "📝 > "
    
    def __init__(self):
        """Initialize the command interface with managers and AI assistant."""
        super().__init__()
        self.task_manager = TaskManager()
        self.knowledge_manager = KnowledgeManager()
        self.ai_assistant = AIAssistant(self.task_manager, self.knowledge_manager)

    def do_task(self, arg):
        """Manage tasks with enhanced features.
        
        Usage:
            task add <title> <description> [priority] [due_date] [#category1,#category2] [@tag1,@tag2]
            task list [all|pending|completed]
            task update <id> <field> <value>
            task complete <id>
            task search <query>
            task view <id>
        """
        args = shlex.split(arg)
        if not args:
            print("Usage: task <command> [arguments]")
            return
        
        command = args[0]
        
        if command == "add" and len(args) >= 3:
            # Parse categories and tags from description
            title = args[1]
            desc = args[2]
            priority = args[3] if len(args) > 3 else "normal"
            due_date = args[4] if len(args) > 4 else None
            
            # Extract categories and tags
            categories = []
            tags = []
            words = desc.split()
            for word in words:
                if word.startswith("#"):
                    categories.append(word[1:])
                elif word.startswith("@"):
                    tags.append(word[1:])
            
            task = self.task_manager.add_task(
                title=title,
                description=desc,
                priority=priority,
                due_date=due_date,
                categories=categories,
                tags=tags
            )
            print(f"✅ Added task #{task.id}: {task.title}")
            
        elif command == "list":
            filter_type = args[1] if len(args) > 1 else "all"
            tasks = self.task_manager.tasks
            
            if filter_type == "pending":
                tasks = [t for t in tasks if t.status != "completed"]
            elif filter_type == "completed":
                tasks = [t for t in tasks if t.status == "completed"]
            
            if not tasks:
                print("No tasks found.")
                return
                
            print("\n📋 Task List:")
            for task in tasks:
                status = "✓" if task.status == "completed" else " "
                print(f"[{status}] #{task.id}: {task.title}")
                print(f"    Priority: {task.priority}")
                if task.due_date:
                    print(f"    Due: {task.due_date}")
                if task.categories:
                    print(f"    Categories: {', '.join(task.categories)}")
                if task.tags:
                    print(f"    Tags: {', '.join(task.tags)}")
                print()
                
        elif command == "update" and len(args) >= 4:
            task_id = int(args[1])
            field = args[2]
            value = args[3]
            
            if self.task_manager.update_task(task_id, **{field: value}):
                print(f"✅ Updated task #{task_id}")
            else:
                print("Task not found.")
                
        elif command == "complete" and len(args) > 1:
            task_id = int(args[1])
            if self.task_manager.update_task(task_id, status="completed"):
                print(f"✅ Marked task #{task_id} as completed")
            else:
                print("Task not found.")
                
        elif command == "search" and len(args) > 1:
            query = args[1]
            results = self.task_manager.search_tasks(query=query)
            
            if results:
                print("\n🔍 Search results:")
                for task in results:
                    print(f"#{task.id}: {task.title}")
            else:
                print("No matching tasks found.")
                
        elif command == "view" and len(args) > 1:
            task_id = int(args[1])
            task = self.task_manager.get_task(task_id)
            
            if task:
                print(f"\n📄 Task #{task.id}: {task.title}")
                print(f"Description: {task.description}")
                print(f"Status: {task.status}")
                print(f"Priority: {task.priority}")
                if task.due_date:
                    print(f"Due: {task.due_date}")
                print(f"Categories: {', '.join(task.categories)}")
                print(f"Tags: {', '.join(task.tags)}")
                print(f"Created: {task.created_at}")
                if task.completed_at:
                    print(f"Completed: {task.completed_at}")
            else:
                print("Task not found.")
        else:
            print("Invalid task command or missing arguments")

    def do_know(self, arg):
        """Manage knowledge entries with enhanced features.
        
        Usage:
            know add <title> <content> [#category1,#category2] [@tag1,@tag2]
            know list [category]
            know search <query>
            know view <id>
            know link <entry_id> <task_id>
        """
        args = shlex.split(arg)
        if not args:
            print("Usage: know <command> [arguments]")
            return
        
        command = args[0]
        
        if command == "add" and len(args) >= 3:
            title = args[1]
            content = args[2]
            
            # Extract categories and tags
            categories = []
            tags = []
            words = content.split()
            for word in words:
                if word.startswith("#"):
                    categories.append(word[1:])
                elif word.startswith("@"):
                    tags.append(word[1:])
            
            entry = self.knowledge_manager.add_entry(
                title=title,
                content=content,
                categories=categories,
                tags=tags
            )
            print(f"✅ Added knowledge entry #{entry.id}: {entry.title}")
            
        elif command == "list":
            category = args[1] if len(args) > 1 else None
            entries = self.knowledge_manager.entries
            
            if category:
                entries = [e for e in entries if category in e.categories]
            
            if not entries:
                print("No knowledge entries found.")
                return
                
            print("\n📚 Knowledge Base:")
            for entry in entries:
                print(f"#{entry.id}: {entry.title}")
                if entry.categories:
                    print(f"    Categories: {', '.join(entry.categories)}")
                if entry.tags:
                    print(f"    Tags: {', '.join(entry.tags)}")
                print()
                
        elif command == "search" and len(args) > 1:
            query = args[1]
            results = self.knowledge_manager.search_entries(query=query)
            
            if results:
                print("\n🔍 Search results:")
                for entry in results:
                    print(f"#{entry.id}: {entry.title}")
            else:
                print("No matching entries found.")
                
        elif command == "view" and len(args) > 1:
            entry_id = int(args[1])
            entry = self.knowledge_manager.get_entry(entry_id)
            
            if entry:
                print(f"\n📄 Entry #{entry.id}: {entry.title}")
                print("-" * 40)
                print(entry.content)
                print("-" * 40)
                print(f"Categories: {', '.join(entry.categories)}")
                print(f"Tags: {', '.join(entry.tags)}")
                if entry.references:
                    print("References:")
                    for ref in entry.references:
                        print(f"- {ref}")
                if entry.related_tasks:
                    print("Related Tasks:")
                    for task_id in entry.related_tasks:
                        task = self.task_manager.get_task(task_id)
                        if task:
                            print(f"- #{task_id}: {task.title}")
            else:
                print("Entry not found.")
                
        elif command == "link" and len(args) > 2:
            entry_id = int(args[1])
            task_id = int(args[2])
            
            if self.knowledge_manager.link_to_task(entry_id, task_id):
                print(f"✅ Linked knowledge entry #{entry_id} to task #{task_id}")
            else:
                print("Entry or task not found.")
        else:
            print("Invalid knowledge command or missing arguments")

    def do_ask(self, arg):
        """Ask the AI assistant for help and insights.
        
        Usage:
            ask brief
            ask suggest
            ask insights
            ask help <topic>
        """
        if not arg:
            print("What would you like to know? Try 'ask brief' or 'ask suggest'")
            return
            
        command = arg.split()[0].lower()
        
        if command == "brief":
            print(self.ai_assistant.get_daily_brief())
        elif command == "suggest":
            print(self.ai_assistant.suggest_next_actions())
        elif command == "insights":
            print(self.ai_assistant.get_productivity_insights())
        elif command == "help":
            topic = " ".join(arg.split()[1:])
            # Add custom help topics here
            print(f"Help information for: {topic}")
        else:
            # General query - try to find relevant tasks and knowledge
            results_found = False
            
            tasks = self.task_manager.search_tasks(query=arg)
            if tasks:
                results_found = True
                print("\n📋 Related Tasks:")
                for task in tasks:
                    print(f"#{task.id}: {task.title}")
            
            entries = self.knowledge_manager.search_entries(query=arg)
            if entries:
                results_found = True
                print("\n📚 Related Knowledge:")
                for entry in entries:
                    print(f"#{entry.id}: {entry.title}")
            
            if not results_found:
                print("I couldn't find anything directly related to your query.")
                print("Try using more specific terms or ask for a daily brief.")

    def do_exit(self, arg):
        """Exit the program."""
        print("\nGoodbye! 👋")
        return True

def main():
    """Start the command interface."""
    CommandInterface().cmdloop()

if __name__ == "__main__":
    main()