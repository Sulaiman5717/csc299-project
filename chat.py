import cmd
import shlex
from typing import List, Optional
from datetime import datetime

from tasks import load_tasks, save_tasks, add_task, list_tasks, search_tasks
from knowledge import load_knowledge, save_knowledge, add_entry, list_entries, search_entries, view_entry
from ai_agent import AIAgent
from chat_logger import ChatLogger

class ChatInterface(cmd.Cmd):
    """Interactive CLI chat interface for tasks and knowledge management."""
    
    intro = """
    Welcome to your Personal Knowledge & Task Management System!
    Type 'help' or '?' to list commands.
    """
    prompt = '🤖 > '

    def do_task(self, arg):
        """Manage tasks: task add|list|search [arguments]
        Examples:
            task add "Complete project report"
            task list
            task search "project"
        """
        args = shlex.split(arg)
        if not args:
            print("Usage: task add|list|search [arguments]")
            return

        command = args[0]
        if command == "add" and len(args) > 1:
            add_task(args[1])
        elif command == "list":
            list_tasks()
        elif command == "search" and len(args) > 1:
            search_tasks(args[1])
        else:
            print("Invalid task command or missing arguments")

    def do_know(self, arg):
        """Manage knowledge: know add|list|search|view [arguments]
        Examples:
            know add "Git Tips" "Common git commands..." "git,reference"
            know list
            know search "git"
            know view 1
        """
        args = shlex.split(arg)
        if not args:
            print("Usage: know add|list|search|view [arguments]")
            return

        command = args[0]
        if command == "add" and len(args) > 2:
            title = args[1]
            content = args[2]
            tags = args[3].split(",") if len(args) > 3 else []
            add_entry(title, content, tags)
        elif command == "list":
            list_entries()
        elif command == "search" and len(args) > 1:
            search_entries(args[1])
        elif command == "view" and len(args) > 1:
            try:
                entry_id = int(args[1])
                view_entry(entry_id)
            except ValueError:
                print("Invalid entry ID")
        else:
            print("Invalid knowledge command or missing arguments")

    def __init__(self):
        """Initialize the chat interface with AI agent."""
        super().__init__()
        self.agent = AIAgent()

    def do_ask(self, arg):
        """Ask a natural language question about your tasks or knowledge.
        Examples:
            ask what tasks are due today
            ask what do I know about git
            ask show me my recent entries
            ask for suggestions
            ask about knowledge gaps
            ask for daily brief
        """
        if not arg:
            print("Please ask a question!")
            return

        query = arg.lower()
        
        # Special AI agent commands
        if "suggest" in query or "what next" in query or "what should i do" in query:
            print(self.agent.suggest_next_actions())
            return
            
        if "gap" in query or "missing" in query:
            print(self.agent.analyze_knowledge_gaps())
            return
            
        if "brief" in query or "summary" in query or "overview" in query:
            print(self.agent.get_daily_brief())
            return
        
        # Regular search
        if "task" in query or "todo" in query or "due" in query:
            print("\nRelevant tasks:")
            search_tasks(query)
        
        if "know" in query or "learn" in query or "find" in query:
            print("\nRelevant knowledge entries:")
            search_entries(query)
            
        # Find relevant knowledge for tasks
        if "task" in query and "knowledge" in query:
            tasks = load_tasks()
            if tasks:
                print("\nFinding relevant knowledge for your tasks:")
                for task in tasks[:3]:  # Look at most recent 3 tasks
                    relevant = self.agent.get_relevant_knowledge(task["description"])
                    if relevant:
                        print(f"\nFor task: {task['description']}")
                        for entry in relevant[:2]:  # Show top 2 relevant entries
                            print(f"- {entry['title']}: {entry['content'][:100]}...")

    def do_exit(self, arg):
        """Exit the chat interface."""
        print("Goodbye! 👋")
        return True

    def do_help(self, arg):
        """List available commands with their descriptions."""
        if not arg:
            print("\nAvailable commands:")
            print("  task  - Manage your tasks")
            print("  know  - Manage your knowledge base")
            print("  ask   - Ask questions in natural language")
            print("  exit  - Exit the program")
            print("\nType 'help <command>' for more details on each command.")
        else:
            super().do_help(arg)

def main():
    """Start the chat interface."""
    ChatInterface().cmdloop()

if __name__ == "__main__":
    main()