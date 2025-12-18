from flask import Flask, request, jsonify, render_template
import sqlite3
import os

app = Flask(__name__)
DB_NAME = "tasks.db"

# ---------- Database ----------
def get_db_connection():
    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    if not os.path.exists(DB_NAME):
        conn = get_db_connection()
        conn.execute("""
            CREATE TABLE tasks (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                title TEXT NOT NULL,
                description TEXT,
                status TEXT DEFAULT 'pending'
            )
        """)
        conn.commit()
        conn.close()

init_db()

# ---------- UI Home ----------
@app.route("/")
def home():
    return render_template("index.html")

# ---------- Health Check ----------
@app.route("/health", methods=["GET"])
def health():
    return jsonify({"status": "UP"}), 200

# ---------- Create Task ----------
@app.route("/tasks", methods=["POST"])
def create_task():
    data = request.get_json()
    title = data.get("title")
    description = data.get("description", "")

    if not title:
        return jsonify({"error": "Title is required"}), 400

    conn = get_db_connection()
    conn.execute(
        "INSERT INTO tasks (title, description) VALUES (?, ?)",
        (title, description)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task created"}), 201

# ---------- Get All Tasks ----------
@app.route("/tasks", methods=["GET"])
def get_tasks():
    conn = get_db_connection()
    tasks = conn.execute("SELECT * FROM tasks").fetchall()
    conn.close()

    return jsonify([dict(task) for task in tasks]), 200

# ---------- Update Task ----------
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    data = request.get_json()
    status = data.get("status")

    if status not in ["pending", "completed"]:
        return jsonify({"error": "Invalid status"}), 400

    conn = get_db_connection()
    conn.execute(
        "UPDATE tasks SET status = ? WHERE id = ?",
        (status, task_id)
    )
    conn.commit()
    conn.close()

    return jsonify({"message": "Task updated"}), 200

# ---------- Delete Task ----------
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    conn = get_db_connection()
    conn.execute("DELETE FROM tasks WHERE id = ?", (task_id,))
    conn.commit()
    conn.close()

    return jsonify({"message": "Task deleted"}), 200

# ---------- App Run ----------
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080)

