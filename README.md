# 🧠 PKMS — AI-Powered Task Management System

PKMS (Personal Knowledge & Task Management System) is a **Python-based command-line application** that helps users manage their daily tasks, track goals, and get AI-driven productivity insights — all directly from the terminal.

It integrates intelligent prioritization, goal tracking, and optional AI coaching to make personal organization simple and smart.

---
## Youtube Video
https://youtu.be/QUMSZWsYg1M
---

## ⚡ Demo Mode Available!

Want to explore PKMS without any setup?  
You can run it locally in **demo mode** using the built-in JSON storage — no database or API keys required!

Try it instantly:
<pre> ```python -m pkms.cli add "Finish CSC299 project" --priority high```
</pre> ```python -m pkms.cli list```

---
Perfect for:

📽️ Presentations and demos

🎓 Learning how AI task systems work

🧩 Exploring command-line interfaces

🪶 Lightweight testing (no setup required)
---
💡 What Is PKMS?

PKMS is a terminal-based AI productivity assistant designed to help you stay organized and focused.
It allows you to:

🗂️ Manage Tasks

Add, list, search, complete, and delete tasks

Assign due dates, priorities, and tags

🧠 Get AI Insights

Automatically prioritize tasks by urgency and importance

Receive AI-powered suggestions for your next focus

Generate weekly summaries of completed work

💾 Store Data Securely

Choose between SQLite (default) and JSON storage

Works fully offline — no internet required
---
🚀 Why Use PKMS?
Enhanced Productivity

Focus on the right tasks using AI prioritization

Plan weeks efficiently with clear summaries

Privacy First

100% local storage — your data never leaves your machine

Optional AI integration when you choose to enable it

Academic and Professional Use

Ideal for students, researchers, and developers

Portable, minimal, and fully open source
---
⚙️ Technology Stack

PKMS is built with simplicity and portability in mind.

Component	Description
Python 3.10+	Core language
SQLite / JSON	Storage backends
Argparse	Command-line interface
Datetime / Pathlib	Scheduling and file management
LLM Adapter (Optional)	AI-driven suggestions and summaries
🧩 Requirements

Python 3.10 or later

macOS, Windows, or Linux

Git (for cloning the repository)
---
🔧 Installation
1. Clone the repository
git clone https://github.com/YOUR_USERNAME/csc299-project.git
cd csc299-project

2. Create a virtual environment
python3 -m venv .venv
source .venv/bin/activate   # macOS/Linux
# or
.venv\Scripts\activate      # Windows

3. Install dependencies
pip install -e .

💻 Usage
Show Help
python -m pkms.cli --help

Add a Task
python -m pkms.cli add "Finish CSC299 project" --priority high --due 2025-11-12 --tag school

List Tasks
python -m pkms.cli list

Search Tasks
python -m pkms.cli search project

Mark Task Complete
python -m pkms.cli done 1

AI Suggestions
python -m pkms.cli suggest

Weekly Summary
python -m pkms.cli weekly-summary
---
🧠 AI Integration (Optional)

PKMS includes an optional AI integration for deeper insights and productivity coaching.

To enable AI features:

export PKMS_ENABLE_LLM=1
export OPENAI_API_KEY=sk-...   # or any OpenAI-compatible API key


Then run:

python -m pkms.cli suggest


The AI will analyze your tasks and provide concise, actionable advice.
---
💾 Storage Configuration

You can choose your preferred storage mode:

Mode	Command	Path	Description
SQLite	--storage sqlite	~/.pkms/tasks.db	Default database storage
JSON	--storage json	~/.pkms/tasks.json	Lightweight file storage

Example:

python -m pkms.cli --storage json add "Try PKMS demo"
---
🧩 How It Works

Input: Add and manage tasks through simple CLI commands

Storage: Tasks are saved locally (SQLite or JSON)

AI Layer: Optional AI agent analyzes and prioritizes tasks

Output: Clear summaries and actionable next steps in your terminal
---
🔍 Key Features
🧾 Task Management

Add, edit, delete, and search tasks

Filter by completion status

Track deadlines, tags, and notes

⚙️ AI Assistance

Smart task prioritization

“Next Best Action” recommendations

Weekly performance insights

🛠️ Storage Options

SQLite for speed and indexing

JSON for lightweight, portable data

🧩 Developer Friendly

Fully modular design under pkms/

Extensible storage and AI modules

Open source and easy to modify

🧱 Future Enhancements

Natural language “Quick Add” ("tomorrow 3pm: study discrete math")

PKMS chat interface for interactive AI conversations

Progress analytics and goal tracking dashboard

Note-linking between tasks and research sources

🧑‍💻 Contributing

We welcome contributions!
To contribute:

Fork this repository

Create a new branch

git checkout -b feature/my-feature


Commit and push your changes

Submit a pull request

🪪 License

MIT License © 2025 Sulaiman Syed
Developed for DePaul University — CSC299: AI Coding Assistants Project

⚠️ Disclaimer

This software is provided “as is” for educational and academic purposes.
Users are responsible for:

Managing their data and API keys securely

Reviewing AI-generated suggestions before acting on them

Complying with all relevant software and data regulations

The maintainers are not responsible for any data loss or misuse.

🌟 Summary

PKMS is an AI-powered productivity assistant built entirely in Python for developers, students, and researchers.
It combines practical task management with intelligent prioritization and optional AI coaching —
simple, private, and powerful — right from your terminal.
