from __future__ import annotations
from datetime import datetime, timedelta
from typing import List, Dict, Any
import re

from .task_manager import TaskManager, Task
from .knowledge_manager import KnowledgeManager, KnowledgeEntry

class AIAssistant:
    """Enhanced AI assistant with improved analysis and suggestions."""
    
    def __init__(self, task_manager: TaskManager, knowledge_manager: KnowledgeManager):
        self.task_manager = task_manager
        self.knowledge_manager = knowledge_manager

    def get_daily_brief(self) -> str:
        """Generate a comprehensive daily briefing."""
        tasks = self.task_manager.tasks
        entries = self.knowledge_manager.entries
        
        # Get tasks due today
        today = datetime.now().date()
        due_today = [t for t in tasks if t.due_date and 
                    datetime.fromisoformat(t.due_date).date() == today]
        
        # Get recent knowledge entries
        recent_entries = sorted(
            entries,
            key=lambda e: e.created_at,
            reverse=True
        )[:5]
        
        sections = ["📋 Daily Brief"]
        
        # Task summary
        sections.append(f"\nTasks due today ({len(due_today)}):")
        for task in due_today:
            sections.append(f"- {task.title} (Priority: {task.priority})")
        
        # Task status breakdown
        status_groups = self.task_manager.get_tasks_by_status()
        sections.append("\nTask Status:")
        for status, tasks in status_groups.items():
            sections.append(f"- {status}: {len(tasks)} tasks")
        
        # Knowledge base updates
        sections.append("\nRecent Knowledge Updates:")
        for entry in recent_entries:
            sections.append(f"- {entry.title}")
        
        # Add suggestions
        sections.append("\n" + self.suggest_next_actions())
        
        return "\n".join(sections)

    def suggest_next_actions(self) -> str:
        """Provide intelligent task suggestions."""
        tasks = self.task_manager.tasks
        if not tasks:
            return "No tasks found. Consider adding some tasks to get started!"
        
        # Sort tasks by priority and due date
        def task_score(task: Task) -> tuple:
            priority_score = {"urgent": 0, "high": 1, "normal": 2, "low": 3}
            due_score = datetime.fromisoformat(task.due_date) if task.due_date else datetime.max
            return (priority_score.get(task.priority, 4), due_score)
        
        active_tasks = [t for t in tasks if t.status != "completed"]
        sorted_tasks = sorted(active_tasks, key=task_score)
        
        suggestions = ["🎯 Suggested Actions:"]
        
        if sorted_tasks:
            # Suggest highest priority task
            top_task = sorted_tasks[0]
            suggestions.append(f"\n1. Focus on: {top_task.title}")
            suggestions.append(f"   Priority: {top_task.priority}")
            if top_task.due_date:
                suggestions.append(f"   Due: {top_task.due_date}")
            
            # Find related knowledge
            related_knowledge = self.find_related_knowledge(top_task)
            if related_knowledge:
                suggestions.append("\n   Relevant knowledge entries:")
                for entry in related_knowledge[:2]:
                    suggestions.append(f"   - {entry.title}")
        
        # Suggest task organization if needed
        unorganized = [t for t in tasks if not t.categories and not t.tags]
        if unorganized:
            suggestions.append("\n2. Organization needed:")
            suggestions.append(f"   {len(unorganized)} tasks need categorization")
        
        return "\n".join(suggestions)

    def find_related_knowledge(self, task: Task) -> List[KnowledgeEntry]:
        """Find knowledge entries related to a task."""
        # Extract keywords from task title and description
        text = f"{task.title} {task.description}"
        keywords = set(re.findall(r'\w+', text.lower()))
        
        # Score each knowledge entry for relevance
        scored_entries = []
        for entry in self.knowledge_manager.entries:
            entry_text = f"{entry.title} {entry.content}"
            entry_words = set(re.findall(r'\w+', entry_text.lower()))
            
            # Calculate relevance score
            common_words = keywords & entry_words
            score = len(common_words) / len(keywords) if keywords else 0
            
            if score > 0.2:  # Minimum relevance threshold
                scored_entries.append((score, entry))
        
        # Return most relevant entries
        return [entry for _, entry in sorted(scored_entries, reverse=True)]

    def analyze_task_patterns(self) -> Dict[str, Any]:
        """Analyze patterns in task completion and categories."""
        completed_tasks = [t for t in self.task_manager.tasks if t.status == "completed"]
        if not completed_tasks:
            return {"message": "No completed tasks to analyze"}
        
        analysis = {}
        
        # Analyze completion times by priority
        priority_times = {"urgent": [], "high": [], "normal": [], "low": []}
        for task in completed_tasks:
            if task.completed_at and task.created_at:
                start = datetime.fromisoformat(task.created_at)
                end = datetime.fromisoformat(task.completed_at)
                duration = (end - start).total_seconds() / 3600  # hours
                priority_times[task.priority].append(duration)
        
        analysis["average_completion_times"] = {
            priority: sum(times) / len(times) if times else 0
            for priority, times in priority_times.items()
        }
        
        # Analyze category distribution
        categories = {}
        for task in completed_tasks:
            for category in task.categories:
                categories[category] = categories.get(category, 0) + 1
        
        analysis["category_distribution"] = categories
        
        return analysis

    def get_productivity_insights(self) -> str:
        """Generate productivity insights based on task and knowledge patterns."""
        analysis = self.analyze_task_patterns()
        
        insights = ["📊 Productivity Insights"]
        
        # Add completion time insights
        if "average_completion_times" in analysis:
            insights.append("\nTask Completion Patterns:")
            for priority, hours in analysis["average_completion_times"].items():
                if hours > 0:
                    insights.append(f"- {priority} tasks: {hours:.1f} hours on average")
        
        # Add category insights
        if "category_distribution" in analysis:
            insights.append("\nMost Active Categories:")
            sorted_cats = sorted(
                analysis["category_distribution"].items(),
                key=lambda x: x[1],
                reverse=True
            )
            for cat, count in sorted_cats[:3]:
                insights.append(f"- {cat}: {count} tasks completed")
        
        return "\n".join(insights)