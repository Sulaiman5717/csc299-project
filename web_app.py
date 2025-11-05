#!/usr/bin/env python3
"""
Flask web app for PKMS task manager.
Run with: python3 web_app.py
Opens browser automatically at http://localhost:5000
"""
from __future__ import annotations

import webbrowser
from pathlib import Path
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from pkms.storage.json_store import JSONStore
from pkms.models import Task

app = Flask(__name__)
app.secret_key = "pkms-secret-key-change-in-production"

# Use demo_tasks.json in repo root by default
DATA_FILE = Path(__file__).parent / "demo_tasks.json"
store = JSONStore(DATA_FILE)


@app.route("/")
def index():
    """Main page: list all tasks."""
    tasks = store.list(include_done=False)
    completed = store.list(include_done=True)
    completed = [t for t in completed if t.done]
    return render_template("index.html", tasks=tasks, completed=completed)


@app.route("/add", methods=["POST"])
def add_task():
    """Add a new task."""
    title = request.form.get("title", "").strip()
    priority = request.form.get("priority", "normal")
    due = request.form.get("due", "").strip()
    tags_raw = request.form.get("tags", "").strip()
    note = request.form.get("note", "").strip()

    if not title:
        flash("Task title is required", "error")
        return redirect(url_for("index"))

    tags = [t.strip() for t in tags_raw.split(",") if t.strip()]
    due_date = None
    if due:
        try:
            from datetime import date
            due_date = date.fromisoformat(due)
        except ValueError:
            flash(f"Invalid due date: {due}", "error")
            return redirect(url_for("index"))

    task = Task(
        id=None,
        title=title,
        priority=priority,
        due=due_date,
        tags=tags,
        note=note or None,
        created_at=datetime.utcnow(),
        done=False,
        done_at=None,
    )
    task_id = store.add(task)
    flash(f"Added task #{task_id}: {title}", "success")
    return redirect(url_for("index"))


@app.route("/done/<int:task_id>")
def mark_done(task_id):
    """Mark a task as done."""
    if store.complete(task_id):
        flash(f"Task #{task_id} marked done", "success")
    else:
        flash(f"Task #{task_id} not found or already done", "error")
    return redirect(url_for("index"))


@app.route("/delete/<int:task_id>")
def delete_task(task_id):
    """Delete a task."""
    if store.delete(task_id):
        flash(f"Task #{task_id} deleted", "success")
    else:
        flash(f"Task #{task_id} not found", "error")
    return redirect(url_for("index"))


@app.route("/suggest")
def suggest():
    """Show AI suggestion for next action."""
    from main import AIAgent
    tasks = store.list(include_done=False)
    agent = AIAgent()
    suggestion = agent.suggest_next_action(tasks)
    return render_template("suggest.html", suggestion=suggestion, tasks=tasks)


def open_browser():
    """Open the browser after a short delay."""
    import time
    time.sleep(1.5)
    webbrowser.open("http://localhost:5001")


if __name__ == "__main__":
    import threading
    threading.Thread(target=open_browser, daemon=True).start()
    print("Starting PKMS web app at http://localhost:5001")
    print("Press Ctrl+C to stop")
    app.run(debug=True, use_reloader=False, port=5001)
