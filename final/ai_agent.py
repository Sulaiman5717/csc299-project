
        # Sort tasks by creation date (assuming newer = more important)
        sorted_tasks = sorted(
            self.tasks,
            key=lambda x: x.get('id', 0),
            reverse=True
        )

        suggestions = ["Here's what I suggest:"]
        
        # Suggest the newest task first
        newest_task = sorted_tasks[0]
        suggestions.append(f"\n1. Focus on your newest task: {newest_task['description']}")
        
        # Find relevant knowledge for the newest task
        relevant_knowledge = self.get_relevant_knowledge(newest_task['description'])
        if relevant_knowledge:
            suggestions.append("\nRelevant knowledge entries that might help:")
            for entry in relevant_knowledge[:2]:  # Show top 2 relevant entries
                suggestions.append(f"- {entry['title']}: {entry['content'][:100]}...")

        # Additional task suggestions
        if len(sorted_tasks) > 1:
            suggestions.append("\nAfter that, consider working on:")
            for task in sorted_tasks[1:3]:  # Next 2 tasks
                suggestions.append(f"- {task['description']}")

        return "\n".join(suggestions)

    def analyze_knowledge_gaps(self) -> str:
        """Identify areas where knowledge might be missing."""
        if not self.tasks or not self.knowledge:
            return "Add some tasks and knowledge entries to get started!"

        # Extract common terms from tasks
        task_terms = set()
        for task in self.tasks:
            terms = re.findall(r'\w+', task['description'].lower())
            task_terms.update(terms)

        # Extract terms from knowledge base
        knowledge_terms = set()
        for entry in self.knowledge:
            terms = re.findall(r'\w+', entry['title'].lower() + ' ' + entry['content'].lower())
            knowledge_terms.update(terms)

        # Find terms in tasks that don't have corresponding knowledge entries
        missing_terms = task_terms - knowledge_terms
        
        if missing_terms:
            suggestions = ["Consider adding knowledge entries about:"]
            for term in list(missing_terms)[:5]:  # Top 5 missing terms
                suggestions.append(f"- {term}")
            return "\n".join(suggestions)
        else:
            return "Your knowledge base seems well-aligned with your tasks!"

    def get_daily_brief(self) -> str:
        """Get a daily briefing of tasks and relevant knowledge."""
        self.refresh_data()  # Ensure we have the latest data
        
        sections = ["📋 Daily Brief"]
        
        # Task summary
        task_count = len(self.tasks)
        sections.append(f"\nTasks: {task_count} total")
        if self.tasks:
            sections.append("Recent tasks:")
            for task in sorted(self.tasks, key=lambda x: x.get('id', 0), reverse=True)[:3]:
                sections.append(f"- {task['description']}")

        # Knowledge summary
        knowledge_count = len(self.knowledge)
        sections.append(f"\nKnowledge Base: {knowledge_count} entries")
        if self.knowledge:
            sections.append("Recent entries:")
            for entry in sorted(self.knowledge, key=lambda x: x['created_at'], reverse=True)[:3]:
                sections.append(f"- {entry['title']}")

        # Add suggestions
        sections.append("\n" + self.suggest_next_actions())
        
        return "\n".join(sections)

def main():
    """Test the AI agent functionality."""
    agent = AIAgent()
    print("Testing AI Agent...")
    print("\n=== Daily Brief ===")
    print(agent.get_daily_brief())
    print("\n=== Knowledge Gap Analysis ===")
    print(agent.analyze_knowledge_gaps())

if __name__ == "__main__":
    main()
