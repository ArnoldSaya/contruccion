from flask import Flask
from models import db, Task, User
import config

def migrate_data():

    # =========================
    # 1. APP PARA MYSQL (ORIGEN)
    # =========================
    app_mysql = Flask(__name__)
    app_mysql.config["SQLALCHEMY_DATABASE_URI"] = config.MYSQL_URI
    app_mysql.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app_mysql)

    with app_mysql.app_context():
        users = User.query.all()
        tasks = Task.query.all()

        print(f"Usuarios encontrados: {len(users)}")
        print(f"Tareas encontradas: {len(tasks)}")

        users_data = [u.to_dict() for u in users]
        tasks_data = [t.to_dict() for t in tasks]

    # =========================
    # 2. APP PARA POSTGRES (DESTINO)
    # =========================
    app_pg = Flask(__name__)
    app_pg.config["SQLALCHEMY_DATABASE_URI"] = config.POSTGRES_URI
    app_pg.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app_pg)

    with app_pg.app_context():
        #rear tablas en PostgreSQL
        db.drop_all()
        db.create_all()

        # Insertar usuarios
        for u in users_data:
            new_user = User(id=u["id"], name=u["name"])
            db.session.add(new_user)

        db.session.commit()

        # Insertar tareas
        for t in tasks_data:
            new_task = Task(
                id=t["id"],
                content=t["content"],
                done=t["done"],
                user_id=t["user_id"]
            )
            db.session.add(new_task)

        db.session.commit()

        print("✅ Migración completada en PostgreSQL")

if __name__ == "__main__":
    migrate_data()