from flask import Flask
from flask import request, jsonify
# Create Flask app
app = Flask(__name__)

tasks = []  # store tasks in memory

# GET - retrieve all tasks
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})

# GET - retrieve all tasks  
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify({"id": task["id"], "content": task["content"]})
    return jsonify({"error": "Task not found"})

# POST - add a new task
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json
    task = {"id": len(tasks), "content": data.get("content", "")}
    tasks.append(task)
    return jsonify({"message": "Task added!", "task": task}), 201

# PUT - update a task by ID
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404
    data = request.json
    tasks[task_id]["content"] = data.get("content", tasks[task_id]["content"])
    return jsonify({"message": "Task updated!", "task": tasks[task_id]})

# DELETE - delete a task by ID
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404
    removed = tasks.pop(task_id)
    return jsonify({"message": "Task deleted!", "task": removed})

if __name__ == "__main__":
    # Start development server
    app.run(debug=True)
