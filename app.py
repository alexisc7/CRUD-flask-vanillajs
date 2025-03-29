import sqlite3
from flask import Flask, g

app = Flask(__name__)


def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect("usersdb.db")
        g.cursor = g.db.cursor()
    return g.cursor


@app.teardown_appcontext
def close_connection(exception):
    db = g.pop('db', None)
    if db is not None:
        db.close()


@app.route('/')
def index():
    cursor = get_db()
    cursor.execute("SELECT 1 + 3")
    result = cursor.fetchone()
    print(result)
    return 'prueba'


if __name__ == '__main__':
    app.run(debug=True)
