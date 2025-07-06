from flask import Flask, render_template, request, redirect, url_for
import json
import os

app = Flask(__name__)

TASKS_FILE = 'tasks.json'


def load_tasks():
    if os.path.exists(TASKS_FILE):
        with open(TASKS_FILE, 'r') as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return []
    return []


def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=2)


@app.route('/')
def index():
    tasks = load_tasks()
    total = len(tasks)
    completed = sum(1 for t in tasks if t["completed"])
    pending = total - completed
    return render_template("index.html", tasks=tasks, total=total, completed=completed, pending=pending)


@app.route('/add', methods=['POST'])
def add():
    task_text = request.form.get("task", "").strip()
    if task_text:
        tasks = load_tasks()
        tasks.append({"task": task_text, "completed": False})
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route('/delete/<int:index>')
def delete(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks.pop(index)
        save_tasks(tasks)
    return redirect(url_for("index"))


@app.route('/toggle/<int:index>')
def toggle(index):
    tasks = load_tasks()
    if 0 <= index < len(tasks):
        tasks[index]["completed"] = not tasks[index]["completed"]
        save_tasks(tasks)
    return redirect(url_for("index"))


if __name__ == '__main__':
    app.run(debug=True, host="0.0.0.0", port=5002)
