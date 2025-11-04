# Tasks2 - Enhanced Personal Knowledge & Task Management System

An improved version of the personal knowledge and task management system with enhanced features and better organization.

## New Features

1. **Enhanced Task Management**
   - Task categories and tags
   - Priority levels
   - Due dates
   - Status tracking
   - Better organization

2. **Improved Knowledge Base**
   - Categories and tags
   - References support
   - Link knowledge to tasks
   - Better search capabilities

3. **Smarter AI Assistant**
   - Daily briefings
   - Task suggestions
   - Knowledge recommendations
   - Productivity insights

4. **Better User Interface**
   - Natural language queries
   - Enhanced command syntax
   - Better output formatting
   - More intuitive commands

## Project Structure

```
tasks2/
├── src/
│   ├── task_manager.py      # Enhanced task management
│   ├── knowledge_manager.py # Improved knowledge base
│   ├── ai_assistant.py      # Smarter AI features
│   └── command_interface.py # Better CLI interface
├── data/                    # Data storage
├── tests/                   # Test suite
└── main.py                 # Entry point
```

## Usage

1. Start the application:
   ```bash
   python main.py
   ```

2. Manage tasks:
   ```bash
   task add "Complete report" "Write project report" high "2025-11-10" #work,#project @docs
   task list
   task search "report"
   task complete 1
   ```

3. Manage knowledge:
   ```bash
   know add "Git Commands" "Common git commands..." #git,#reference @commands
   know list
   know search "git"
   know link 1 2  # Link knowledge to task
   ```

4. Get AI assistance:
   ```bash
   ask brief      # Get daily briefing
   ask suggest    # Get task suggestions
   ask insights   # Get productivity insights
   ```

## Improvements from v1

1. Better code organization and modularity
2. Enhanced data models with more metadata
3. Improved search capabilities
4. Better AI suggestions and insights
5. More intuitive command interface
6. Cross-platform compatibility
7. Better error handling

## Development

The code is organized into modules for better maintainability and testing. Key improvements include:

1. Use of dataclasses for better data modeling
2. Pathlib for cross-platform file handling
3. Type hints for better code quality
4. Enhanced error handling
5. Better separation of concerns