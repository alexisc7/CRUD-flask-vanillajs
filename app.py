import sqlite3
from flask import Flask, g, request, jsonify
from werkzeug.security import generate_password_hash


app = Flask(__name__)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("usersdb.db")
        g.db.row_factory = sqlite3.Row
        g.cursor = g.db.cursor()
    return g.db, g.cursor


@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.get('/api/users')
def get_users():
    return 'getting users'


@app.post('/api/users')
def create_user():
    new_user = request.get_json()
    username = new_user['username']
    email = new_user['email']
    password = generate_password_hash(new_user['password'])

    db, cursor = get_db()
    cursor.execute('INSERT INTO users (username, email, password) VALUES (?, ?, ?) RETURNING *',
                   (username, email, password))
    new_created_user = cursor.fetchone()
    db.commit()
    return jsonify(dict(new_created_user))


@app.put('/api/users/<int:id>')
def update_user(id):
    return 'updating user {}'.format(id)


@app.delete('/api/users/1')
def delete_user():
    return 'deleting user'


@app.get('/api/users/<int:id>')
def get_user(id):
    return 'getting user {}'.format(id)



if __name__ == '__main__':
    app.run(debug=True)
