from flask import Flask, request, jsonify
from flask_cors import CORS

app = Flask(__name__)
CORS(app)
tasks = []  # store tasks in memory
users = []  # store users in memory

# =========================
# TASKS
# =========================

# GET - Obtiene todas las tareas
@app.route("/tasks", methods=["GET"])
def get_tasks():
    return jsonify({"tasks": tasks})

# GET - Obtiene una tarea por ID 
@app.route("/tasks/<int:task_id>", methods=["GET"])
def get_task(task_id):
    for task in tasks:
        if task["id"] == task_id:
            return jsonify(task)
    return jsonify({"error": "Task not found"}), 404

# POST - Crea una nueva tarea (con validación)
@app.route("/tasks", methods=["POST"])
def add_task():
    data = request.json

    # VALIDACIÓN: no permitir tareas vacías
    if not data or not data.get("content"):
        return jsonify({"error": "Content cannot be empty"}), 400

    task = {
        "id": len(tasks),
        "content": data["content"],
        "done": False
    }
    tasks.append(task)
    return jsonify({"message": "Task added!", "task": task}), 201

# PUT - Actualiza una tarea por ID 
@app.route("/tasks/<int:task_id>", methods=["PUT"])
def update_task(task_id):
    if task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404

    data = request.json

    if "content" in data:
        tasks[task_id]["content"] = data["content"]

    if "done" in data:
        tasks[task_id]["done"] = data["done"]

    return jsonify({"message": "Task updated!", "task": tasks[task_id]})

# PATCH - marcar tarea como completada
@app.route("/tasks/<int:task_id>/complete", methods=["PATCH"])
def mark_complete(task_id):
    if task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404

    tasks[task_id]["done"] = True
    return jsonify({"message": "Task marked as completed", "task": tasks[task_id]})

# DELETE - delete a task by ID
@app.route("/tasks/<int:task_id>", methods=["DELETE"])
def delete_task(task_id):
    if task_id >= len(tasks):
        return jsonify({"error": "Task not found"}), 404

    removed = tasks.pop(task_id)
    return jsonify({"message": "Task deleted!", "task": removed})


# =========================
# USERS
# =========================

# GET - list all users (JSON)
@app.route("/users", methods=["GET"])
def get_users():
    return jsonify({"users": users})

# GET - get user by ID (FORMATO SIMPLE PARA NAVEGADOR)
@app.route("/users/<int:user_id>", methods=["GET"])
def get_user(user_id):
    for user in users:
        if user["id"] == user_id:
            address = user["address"]
            texto = f'{user["name"]} {user["lastname"]} {address["city"]} {address["country"]} {address["code"]}'
            return texto
    return "User not found", 404

# POST - create user
@app.route("/users", methods=["POST"])
def create_user():
    data = request.json

    user = {
        "id": len(users),
        "name": data.get("name"),
        "lastname": data.get("lastname"),
        "address": {
            "city": data.get("address", {}).get("city"),
            "country": data.get("address", {}).get("country"),
            "code": data.get("address", {}).get("code")
        }
    }

    users.append(user)
    return jsonify({"message": "User created!", "user": user}), 201

# PUT - update user
@app.route("/users/<int:user_id>", methods=["PUT"])
def update_user(user_id):
    if user_id >= len(users):
        return jsonify({"error": "User not found"}), 404

    data = request.json

    if "name" in data:
        users[user_id]["name"] = data["name"]

    if "lastname" in data:
        users[user_id]["lastname"] = data["lastname"]

    if "address" in data:
        users[user_id]["address"] = data["address"]

    return jsonify({"message": "User updated!", "user": users[user_id]})

# DELETE - delete user
@app.route("/users/<int:user_id>", methods=["DELETE"])
def delete_user(user_id):
    if user_id >= len(users):
        return jsonify({"error": "User not found"}), 404

    removed = users.pop(user_id)
    return jsonify({"message": "User deleted!", "user": removed})



@app.route("/")
def home():
    return "API funcionando correctamente"


if __name__ == "__main__":
    app.run(debug=True)