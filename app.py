import sqlite3
from flask import Flask, g, request, jsonify
from werkzeug.security import generate_password_hash

app = Flask(__name__)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect("usersdb.db")
        g.db.row_factory = sqlite3.Row
        g.cursor = g.db.cursor()
    return g.db, g.cursor


@app.teardown_appcontext
def close_connection(exception):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def serialize_row(row):
    return {
        key: (row[key].decode("utf-8")
              if isinstance(row[key], bytes) else row[key])
        for key in row.keys()
    }


@app.get("/api/users")
def get_users():
    _, cursor = get_db()
    cursor.execute("SELECT * FROM users")
    users = cursor.fetchall()
    users_list = [serialize_row(user) for user in users]
    return jsonify(users_list)


@app.post("/api/users")
def create_user():
    new_user = request.get_json()
    username = new_user["username"]
    email = new_user["email"]
    password = generate_password_hash(new_user["password"])

    db, cursor = get_db()
    cursor.execute(
        "INSERT INTO users (username, email, password) VALUES (?, ?, ?) RETURNING *",
        (username, email, password),
    )
    new_created_user = cursor.fetchone()
    db.commit()

    user_dict = serialize_row(new_created_user)
    return jsonify(user_dict)


@app.put("/api/users/<int:id>")
def update_user(id):
    db, cursor = get_db()
    new_user_data = request.get_json()
    username = new_user_data["username"]
    email = new_user_data["email"]
    password = generate_password_hash(new_user_data["password"])
    cursor.execute('UPDATE users SET username = ?, email = ?, password = ? WHERE id = ? RETURNING *', 
                   (username, email, password, id))
    updated_user = cursor.fetchone()

    if updated_user is None:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    db.commit()
    return jsonify({"message": "Usuario actualizado con éxito",
                    "usuario_actualizado": serialize_row(updated_user)
                    }), 200


@app.delete("/api/users/<int:id>")
def delete_user(id):
    db, cursor = get_db()
    cursor.execute("DELETE FROM users WHERE id = ? RETURNING *", (id,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({"message": "Usuario no encontrado"}), 404
    
    db.commit()
    return jsonify({"message": "Usuario eliminado con éxito",
                    "usuario_eliminado": serialize_row(user)
                    }), 200


@app.get("/api/users/<int:id>")
def get_user(id):
    _, cursor = get_db()
    cursor.execute("SELECT * FROM users WHERE id = ?", (id,))
    user = cursor.fetchone()
    if user is None:
        return jsonify({"message": "Usuario no encontrado"}), 404
    return jsonify(serialize_row(user)), 200


if __name__ == "__main__":
    app.run(debug=True)