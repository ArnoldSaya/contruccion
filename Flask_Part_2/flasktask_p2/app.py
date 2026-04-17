from flask import Flask, request, jsonify
from models import db, Task, User
from datetime import datetime
import config

def create_app():
    app = Flask(__name__)

    app.config["SQLALCHEMY_DATABASE_URI"] = config.MYSQL_URI
    #app.config["SQLALCHEMY_DATABASE_URI"] = config.POSTGRES_URI
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = config.SQLALCHEMY_TRACK_MODIFICATIONS
    app.config["SECRET_KEY"] = config.SECRET_KEY

    db.init_app(app)

    # ---------- Health & Root ----------
    @app.route("/")
    def root():
        return jsonify({"message": "Task Manager API (Flask + MySQL + SQLAlchemy)"}), 200

    @app.route("/healthz")
    def health():
        # Lightweight health check
        return jsonify({"status": "ok"}), 200

    # =========================
    # USERS
    # =========================
    @app.route("/users", methods=["GET"])
    def list_users():
        users = User.query.all()
        return jsonify([u.to_dict() for u in users]), 200

    @app.route("/users", methods=["POST"])
    def create_user():
        data = request.get_json()

        new_user = User(name=data["name"])
        db.session.add(new_user)
        db.session.commit()

        return jsonify(new_user.to_dict()), 201
    
    @app.route("/users/<int:user_id>", methods=["GET"])
    def get_user(user_id):
        user = User.query.get_or_404(user_id)
        return jsonify(user.to_dict()), 200
    
    @app.route("/users/<int:user_id>", methods=["PUT"])
    def update_user(user_id):
        user = User.query.get_or_404(user_id)
        data = request.get_json()

        user.name = data.get("name", user.name)
        db.session.commit()

        return jsonify(user.to_dict()), 200
    
    @app.route("/users/<int:user_id>", methods=["DELETE"])
    def delete_user(user_id):
        user = User.query.get_or_404(user_id)

        # eliminar tareas del usuario
        for task in user.tasks:
            db.session.delete(task)

        db.session.delete(user)
        db.session.commit()

        return jsonify({"message": "Usuario y sus tareas eliminados"}), 200
    
    # =========================
    # TASKS
    # =========================
    @app.route("/tasks", methods=["GET"])
    def list_tasks():
       
        page = request.args.get("page",1,type=int)
        limit = request.args.get("limit",20,type=int)
        query = request.args.get("query", None, type=str)
        #Solo tareas no eliminadas
        base_query = Task.query.filter(Task.deleted_at.is_(None))

        if query:
            base_query = base_query.filter(Task.content.ilike(f"%{query}%"))
        
        paginacion = base_query.paginate( page=page, per_page=limit, error_out=False)

        return jsonify({
            "page":page,
            "limit":limit,
            "total":paginacion.total,
            "pages":paginacion.pages,
            "data":[t.to_dict() for t in paginacion.items]
        }), 200
    
    @app.route("/tasks", methods=["POST"])
    def create_task():
        data = request.get_json()

        new_task = Task(
            content=data["content"],
            done=data.get("done", False),
            user_id=data["user_id"]
        )

        db.session.add(new_task)
        db.session.commit()

        return jsonify(new_task.to_dict()), 201

    @app.route("/tasks/<int:task_id>", methods=["GET"])
    def get_task(task_id):
        task = Task.query.get_or_404(task_id)
        return jsonify(task.to_dict()), 200

    @app.route("/tasks/<int:task_id>", methods=["PUT"])
    def update_task(task_id):
        task = Task.query.get_or_404(task_id)
        data = request.get_json()

        task.content = data.get("content", task.content)
        task.done = data.get("done", task.done)

        db.session.commit()

        return jsonify(task.to_dict()), 200

    @app.route("/tasks/<int:task_id>", methods=["DELETE"])
    def delete_task(task_id):
        task = Task.query.get_or_404(task_id)
        task.deleted_at = datetime.utcnow()
        #db.session.delete(task)
        db.session.commit()

        return jsonify({"message": "Task eliminada(soft delete)"}), 200

    return app


# =========================
# MAIN
# =========================
if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)